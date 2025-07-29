from dataclasses import dataclass, field, replace
from typing import List, Literal
from collections.abc import Iterable

from polars import LazyFrame

from ._utils.normalise import normalise_column_headers
from ..types import (
    ColumnNode,
    SourceColDef,
    ThresholdLevel,
    ValidationResult,
    ProcessingFailure,
    ProcessingSuccess,
)
from .._utils.args import flatten_args
from .._utils.sanitize import sanitise_column_name
from ..column import ColumnSchema
from ..registry import ColumnRegistry, generate_optimized_stages


@dataclass(frozen=True, kw_only=True)
class _SchemaParams:
    name: str
    is_required: bool = False
    stage: str | None = None
    source_columns: dict[str, SourceColDef] = field(default_factory=dict)
    registry: ColumnRegistry = field(default_factory=ColumnRegistry)


class TableSchema:
    """
    Defines a table schema for data validation and processing.

    Parameters:
        name (str): Name of the schema.
        columns (List[ColumnSchema] | dict[str, ColumnSchema], optional): List of column schemas.
        is_required (bool): Whether the schema is required.
        stage (str, optional): Processing stage.

    Usage:
        demo_schema = z.schema("demo", columns=[...])
    """

    def __init__(
        self,
        name: str,
        columns: Iterable[ColumnSchema] | dict[str, ColumnSchema] | None = None,
        *,
        is_required: bool = False,
        stage: str | None = None,
    ):
        cols = _parse_columns_into_list(columns)
        nodes = _cols_to_nodes(schema=name, stage=stage, columns=cols)

        self._params = _SchemaParams(
            name=name,
            is_required=is_required,
            stage=stage,
            registry=ColumnRegistry(nodes),
            source_columns=_cols_to_sources(cols),
        )

    def columns(
        self,
        *args: ColumnSchema | Iterable[ColumnSchema] | dict[str, ColumnSchema],
        method: Literal["merge", "replace"] = "merge",
        **kwargs: ColumnSchema,
    ) -> "TableSchema":
        """Add or replace columns in the schema.

        Args:
            *args: ColumnSchema objects, lists of ColumnSchema, or dicts mapping names to ColumnSchema
            method: Either "merge" to add to existing columns or "replace" to replace all columns
            **kwargs: Named ColumnSchema objects where the key is the column name

        Returns:
            TableSchema: A new schema with the updated columns
        """
        cols = _parse_columns_into_list(*args, **kwargs)

        if method == "merge":
            new_nodes = _cols_to_nodes(
                self._params.name, self._params.stage, columns=cols
            )
            new_registry = _reset_registry(self._params.registry.nodes() + new_nodes)
            new_source_columns = {
                **self._params.source_columns,
                **_cols_to_sources(cols),
            }
            return self._replace(
                registry=new_registry, source_columns=new_source_columns
            )
        elif method == "replace":
            new_registry = _reset_registry(
                _cols_to_nodes(self._params.name, self._params.stage, columns=cols)
            )
            new_source_columns = _cols_to_sources(cols)
            return self._replace(
                registry=new_registry, source_columns=new_source_columns
            )
        else:
            raise ValueError(f"Invalid method: {method}")

    def required(self, is_required: bool = True) -> "TableSchema":
        """Set the schema as required"""
        return self._replace(is_required=is_required)

    @property
    def name(self) -> str:
        """Get the name of the table schema"""
        return self._params.name

    @property
    def is_required(self) -> bool:
        """Get the required status of the table schema"""
        return self._params.is_required

    @property
    def stage(self) -> str:
        """Get the stage of the table schema"""
        return self._params.stage

    def step_1_normalise(
        self, lf: LazyFrame, *, source_name: str | None = None
    ) -> ValidationResult:
        """
        Normalises the provided Polars LazyFrame to ensure column headers align with the
        defined schema/column definitions. It will attempt to rename columns based on
        the column aliases, if column headers are missing it will add them, and drop any
        additional column not defined in the schema.

        Args:
            lf (LazyFrame): The input lazy frame to be normalised.
            source_name (str | None): Optional name of the source for populating error messages.

        Returns:
            ValidationResult: The result of the normalization process, including the
            normalized lazy frame and any errors encountered during the process.

        """
        source_columns = list(self._params.source_columns.values())
        return normalise_column_headers(
            lf.lazy(),
            schema_name=self._params.name,
            col_defs=source_columns,
            source_name=source_name,
        )

    def step_2_prepare(
        self, lf: LazyFrame, *, source_name: str | None = None
    ) -> ValidationResult:
        """
        Applies optimized transformations to the provided Polars LazyFrame (lf). This function
        uses the column definitions to create cleaned & derived/calculated columns, and create
        check columns based on the validation rules defined for each column.

        Args:
            lf (LazyFrame): The input LazyFrame to be processed.
            source_name (str | None): Optional name of the source for populating error messages.

        Returns:
            ValidationResult: The result of the preparation process, including the
            processed LazyFrame and any errors encountered during the process.
        """
        prepped = lf

        stages = generate_optimized_stages(self._params.registry.nodes())

        for stage in stages:
            prepped = prepped.with_columns([c.expression for c in stage])

        # TODO: Add a check to see if the processing stages succeed
        return ValidationResult(data=prepped, errors=[], reject=False)

    def step_3_validate(
        self, lf: LazyFrame, *, source_name: str | None = None
    ) -> ValidationResult:
        """
        Applies validation rules to the provided Polars LazyFrame (lf) based on the column definitions.
        This uses the check columns created in step 2 and applies the validation thresholds to determine
        the resulting validation status/level. The returned LazyFrame isn't modified, but should only be used
        if the entire validation process succeeds without any `reject` level errors.

        Args:
            lf (LazyFrame): The input LazyFrame to be validated.
            source_name (str | None): Optional name of the source for populating error messages.

        Returns:
            ValidationResult: The result of the validation process, including the
            validated LazyFrame and any errors encountered during the process.
        """
        validation_errors = []
        reject = False
        for c in self._params.registry.nodes():
            if c.validation_rule is None:
                continue
            check = c.validation_rule.validate(lf, source=source_name)
            if check is not None:
                validation_errors.append(check)
                if check.level == ThresholdLevel.REJECT.level:
                    reject = True

        return ValidationResult(data=lf, errors=validation_errors, reject=reject)

    def process_data(
        self, lf: LazyFrame, *, source_name: str | None = None
    ) -> ProcessingFailure | ProcessingSuccess:
        """
        Processes data through multiple stages: normalisation, preparation, and validation.
        Each stage processes the input data and checks for errors. If any stage fails,
        the process aborts, returning the stage results and a failure status. If all stages
        are successful, the method returns a success status with all intermediate and final
        results.

        Args:
            lf (LazyFrame): LazyFrame containing the data to be processed.
            source_name (str | None): Optional name of the source for populating error messages.

        Returns:
            ProcessingResult: If any stage (`normalise`, `prepare`, or `validate`) fails with a `reject`,
            returns a `ProcessingFailure` containing intermediate results, encountered errors, and
            the name of the failed stage. Otherwise, returns a `ProcessingSuccess` containing
            intermediate and final results, as well as collected errors during processing.
        """
        errors = []
        normalised = self.step_1_normalise(lf, source_name=source_name)
        errors.extend(normalised.errors)
        if normalised.reject:
            return ProcessingFailure(
                normalised=normalised.data,
                prepared=None,
                validated=None,
                errors=errors,
                failed_stage="normalise",
            )

        prepped = self.step_2_prepare(normalised.data, source_name=source_name)
        errors.extend(prepped.errors)
        if prepped.reject:
            return ProcessingFailure(
                normalised=normalised.data,
                prepared=prepped.data,
                validated=None,
                errors=errors,
                failed_stage="prepare",
            )

        valid = self.step_3_validate(prepped.data, source_name=source_name)
        errors.extend(valid.errors)

        if valid.reject:
            return ProcessingFailure(
                normalised=normalised.data,
                prepared=prepped.data,
                validated=None,
                errors=errors,
                failed_stage="validate",
            )

        # If we get here, the data is valid
        return ProcessingSuccess(
            normalised=normalised.data,
            prepared=prepped.data,
            validated=valid.data,
            errors=errors,
        )

    def _replace(self, **kwargs):
        if "registry" not in kwargs:
            stage = kwargs.get("stage", self._params.stage)
            name = kwargs.get("name", self._params.name)
            kwargs["registry"] = ColumnRegistry(
                [
                    replace(n, stage=stage, schema=name)
                    for n in self._params.registry.nodes()
                ]
            )

        new_params = replace(self._params, **kwargs)
        return TableSchema(name=new_params.name).__set_params(new_params)

    def __set_params(self, params: _SchemaParams) -> "TableSchema":
        self._params = params
        return self


def _cols_to_nodes(
    schema: str, stage: str | None = None, columns: List[ColumnSchema] | None = None
) -> List[ColumnNode]:
    nodes = []
    if columns is None:
        return nodes

    for c in columns:
        assert isinstance(c, ColumnSchema), (
            f"All columns must be a Column Schema definition - {c}"
        )
        assert c.ref.base_name is not None, """
        All Columns must have a name, either:
          - directly on creation, e.g. z.col("name")
          - assigning after creation, e.g. z.col().with_name("name")
          - defined through a keyword arg on schema.columns e.g. x.columns( name = z.col() )
          - defined through a dict key on schema.columns e.g. x.columns({ "name": z.col() })
        """
        nodes.extend(c.get_nodes(schema, stage))

    return nodes


def _cols_to_sources(columns: List[ColumnSchema] | None) -> dict[str, SourceColDef]:
    sources = {}
    aliases = {}
    if columns is None:
        return sources
    for c in columns:
        if c.has_expression:
            # if a column has an expression, it is not a source column
            continue

        ref = c.ref

        if ref.name in sources:
            raise ValueError(f"Duplicate source column name: {ref.name}")
        else:
            col_aliases = {sanitise_column_name(a) for a in c.get_aliases}
            col_aliases.add(sanitise_column_name(ref.name))

            # Check if the alias is already in use
            for a in col_aliases:
                if a in aliases:
                    raise ValueError(
                        f"Duplicate column alias: The sanitized alias `{a}` for column `{ref.name}` already used for `{aliases[a]}`"
                    )
                else:
                    aliases[a] = ref.name

            sources[ref.name] = SourceColDef(
                name=ref.name,
                aliases=col_aliases,
                if_missing=c.if_missing,
                is_meta=c.ref.is_meta,
            )

    return sources


def _reset_registry(nodes: List[ColumnNode], **kwargs):
    return ColumnRegistry([replace(n, **kwargs) for n in nodes])


def _parse_columns_into_list(
    *args: ColumnSchema | Iterable[ColumnSchema] | dict[str, ColumnSchema],
    **kwargs: ColumnSchema,
) -> List[ColumnSchema]:
    cols = []
    # Process positional arguments
    for arg in args:
        if arg is None:
            continue
        if isinstance(arg, dict):
            # Handle dict input like {a: z.col, b: z.col}
            cols.extend(c.with_name(k) for k, c in arg.items())
        elif isinstance(arg, list):
            # Handle list input like [z.col("a"), z.col("b")]
            cols.extend(arg)
        else:
            # Handle single ColumnSchema like z.col("a")
            cols.append(arg)

    # Process keyword arguments
    cols.extend(c.with_name(k) for k, c in kwargs.items())

    return cols
