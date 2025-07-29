import importlib
import inspect
import json
import logging
import pathlib
import sys
import threading
import types
from collections import defaultdict
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from dataclasses import dataclass, field
from tempfile import TemporaryDirectory
from typing import Callable, Optional

import polars as pl
from polars.testing import assert_frame_equal

from blueno.etl.load import append, incremental, overwrite, replace_range, upsert
from blueno.etl.transform import apply_scd_type_2
from blueno.etl.types import DataFrameType

logger = logging.getLogger(__name__)


class GenericBlueprintError(Exception):
    pass


class DuplicateBlueprintError(Exception):
    pass


class InvalidBlueprintDependencyError(Exception):
    pass


@dataclass
class BlueprintRegistry:
    _instance: Optional["BlueprintRegistry"] = None
    blueprints: dict[str, "Blueprint"] = field(default_factory=dict)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def discover_blueprints(self, path: str | pathlib.Path = "blueprints") -> None:
        logger.debug(f"Discovering blueprints in {path}")
        base_dir = pathlib.Path(path).absolute()

        logger.debug(f"Base dir: {base_dir}")

        files = base_dir.rglob("**/*.py")
        import os

        cwd = os.getcwd()
        logger.debug(f"Files: {list(files)}")

        for py_file in base_dir.rglob("**/*.py"):
            # Skip __init__.py or hidden files
            if py_file.name.startswith("__"):
                continue

            module_path = py_file.with_suffix("")

            # Make module path relative to cwd
            module_path = module_path.relative_to(cwd)

            module_name = ".".join(module_path.parts)

            # TODO: Find a better way to do this
            if "." not in sys.path:
                sys.path.append(".")
                importlib.import_module(module_name)
                sys.path.remove(".")
            else:
                importlib.import_module(module_name)

    def register(self, blueprint: "Blueprint") -> None:
        if blueprint.name in self.blueprints:
            msg = f"A blueprint with name {blueprint.name} already exists!"
            logger.error(msg)
            raise DuplicateBlueprintError(f"A blueprint with name {blueprint.name} already exists!")

        self.blueprints[blueprint.name] = blueprint

    def validate_dependencies(self) -> None:
        pass
        # for blueprint in self.blueprints.values():
        #     for dependency in blueprint.depends_on:
        #         if self.blueprints.get(dependency) is None:
        #             from difflib import get_close_matches

        #             close_matches = get_close_matches(dependency, self.blueprints.keys(), n=1)
        #             msg = f"The dependency in blueprint `{blueprint.name}` with name `{dependency}` does not exist!"

        #             if len(close_matches) > 0:
        #                 msg += f" Did you mean `{close_matches[0]}`?"

        #             logger.error(msg)
        #             raise InvalidBlueprintDependencyError(msg)

    def render_dag(self):
        try:
            import graphviz
        except ImportError:
            logger.error("Graphviz is not installed. Please install it to render the DAG.")
            return
        dot = graphviz.Digraph()

        for step in self.blueprints.values():
            dot.node(step.name)
            for dep in step.depends_on:
                dot.edge(dep.name, step.name)

        with TemporaryDirectory() as tmpdirname:  # ty: ignore[no-matching-overload]
            dot.render(tmpdirname + "_dag", view=True, format="png")

    def run(self, subset: list[str] | None, concurrency: int = 1):
        blueprints = list(self.blueprints.values())
        _subset = subset or self.blueprints.keys()
        in_degrees = {step.name: 0 for step in blueprints}
        dependents = defaultdict(list)
        failed_steps = set()
        completed = set()
        lock = threading.Lock()

        for blueprint in blueprints:
            for dep in blueprint.depends_on:
                in_degrees[blueprint.name] += 1
                dependents[dep.name].append(blueprint.name)

        ready = [step for step in blueprints if in_degrees[step.name] == 0]
        running_futures: dict[Future[str], Blueprint] = {}

        def run_step(blueprint: Blueprint):
            logger.info(f"Running: {blueprint.name}")
            try:
                blueprint.run()
            except Exception as e:
                logger.error(f"Error running blueprint {blueprint.name}: {str(e)}")
                with lock:
                    failed_steps.add(blueprint.name)

                raise e
            logger.info(f"Finished: {blueprint.name}")
            return blueprint.name

        with ThreadPoolExecutor(max_workers=concurrency) as executor:
            while ready or running_futures:
                # Submit all ready steps
                if failed_steps:
                    break

                for blueprint in ready:
                    if blueprint.name in _subset:
                        future = executor.submit(run_step, blueprint)
                    else:
                        future = executor.submit(lambda: None)
                    running_futures[future] = blueprint
                ready.clear()

                # Wait for at least one to complete
                done, _ = wait(running_futures.keys(), return_when=FIRST_COMPLETED)
                for future in done:
                    blueprint = running_futures.pop(future)
                    finished_name = blueprint.name
                    with lock:
                        completed.add(finished_name)
                        for dependent_name in dependents[finished_name]:
                            in_degrees[dependent_name] -= 1
                            if in_degrees[dependent_name] == 0:
                                ready.append(self.blueprints[dependent_name])


blueprint_registry = BlueprintRegistry()


@dataclass
class Blueprint:
    name: str
    table_uri: str | None
    schema: pl.Schema | None
    format: str
    write_mode: str
    _transform_fn: Callable
    primary_keys: list[str] = field(default_factory=list)
    incremental_column: str | None = None
    valid_from_column: str | None = None
    valid_to_column: str | None = None

    _depends_on: list["Blueprint"] = field(default_factory=list)
    _dataframe: DataFrameType | None = field(init=False, repr=False, default=None)

    @property
    def depends_on(self) -> list["Blueprint"]:
        sig = inspect.signature(self._transform_fn)

        dependencies = list(sig.parameters.keys())

        inputs = []
        for dependency in dependencies:
            if dependency == "self":
                continue

            blueprint = blueprint_registry.blueprints.get(dependency)
            if blueprint is None:
                msg = f"The dependency in blueprint `{self.name}` with name `{dependency}` does not exist!"
                logger.error(msg)
                raise InvalidBlueprintDependencyError(msg)

            inputs.append(blueprint)
            logger.debug(f"Found dependency: {dependency}, {blueprint}")

        return inputs

    def __str__(self):
        return json.dumps(
            {
                "name": self.table_uri,
                # "depends_on": self.depends_on,
                "primary_keys": self.primary_keys,
                "format": self.format,
                "write_method": self.write_mode,
                "transform_fn": self._transform_fn.__name__,
            }
        )

    def read(self) -> DataFrameType:
        if self._dataframe is not None:
            logger.debug(f"Reading blueprint `{self.name}` from `self._dataframe`")
            return self._dataframe

        if self.table_uri is not None:
            logger.debug(f"Reading blueprint `{self.name}` from `self.table_uri`")
            return self.target_df

        logger.debug(f"Reading blueprint `{self.name}` from `self.transform()`")
        self.transform()

        return self._dataframe

    @property
    def target_df(self) -> DataFrameType:
        return pl.scan_delta(self.table_uri)

    def write(self) -> None:
        logger.debug(
            f"Writing blueprint `{self.name}` to `{self.table_uri}` with mode `{self.write_mode}`"
        )
        match self.write_mode:
            case "append":
                append(
                    table_or_uri=self.table_uri,
                    df=self._dataframe,
                )
            case "incremental":
                incremental(
                    table_or_uri=self.table_uri,
                    df=self._dataframe,
                    incremental_column=self.incremental_column,
                )
            case "replace_range":
                replace_range(
                    table_or_uri=self.table_uri,
                    df=self._dataframe,
                    range_column=self.incremental_column,
                )
            case "overwrite":
                overwrite(
                    table_or_uri=self.table_uri,
                    df=self._dataframe,
                )
            case "upsert":
                upsert(
                    table_or_uri=self.table_uri,
                    df=self._dataframe,
                    primary_key_columns=self.primary_keys,
                )
            case "scd2":
                upsert_df = apply_scd_type_2(
                    source_df=self._dataframe,
                    target_df=self.target_df,
                    primary_key_columns=self.primary_keys,
                    valid_from_column=self.valid_from_column,
                    valid_to_column=self.valid_to_column,
                )
                upsert(
                    table_or_uri=self.table_uri,
                    df=upsert_df,
                    primary_key_columns=self.primary_keys + [self.valid_from_column],
                )
            case _:
                msg = f"Invalid write mode `{self.write_mode}` for blueprint `{self.name}`"
                logger.error(msg)
                raise GenericBlueprintError(msg)

        logger.debug(f"Successfully wrote blueprint `{self.name}` to `{self.table_uri}`")

    def transform(self) -> None:
        logger.debug(f"Transforming blueprint {self.name}")

        dataframes = [input.read() for input in self.depends_on]

        sig = inspect.signature(self._transform_fn)
        if "self" in sig.parameters.keys():
            self._dataframe = self._transform_fn(self, *dataframes)
        else:
            self._dataframe = self._transform_fn(*dataframes)

        if not isinstance(self._dataframe, DataFrameType):
            msg = (
                f"Transform function `{self._transform_fn.__name__}` must return a `DataFrameType`!"
            )
            logger.error(msg)
            raise TypeError(msg)

    def validate_schema(self) -> None:
        if self.schema is None:
            logger.debug(f"Schema is not set for blueprint `{self.name}`. Skipping validation.")
            return

        if self._dataframe is None:
            msg = f"Blueprint `{self.name}` has no dataframe to validate against the schema. Run the `transform` method first!"
            logger.error(msg)
            raise GenericBlueprintError(msg)

        logger.debug(f"Validating schema for blueprint `{self.name}`")

        schema_frame = pl.DataFrame(schema=self.schema)
        assert_frame_equal(self._dataframe.limit(0), schema_frame, check_column_order=False)
        logger.debug(f"Schema validation passed for blueprint `{self.name}`")

    def run(self):
        logger.debug(f"Running blueprint: {self.name}")
        self.transform()
        self.validate_schema()
        self.write()

        logger.debug(f"Succesfully ran blueprint: {self.table_uri}")


def blueprint(
    name: str | None = None,
    table_uri: str | None = None,
    schema: pl.Schema | None = None,
    primary_keys: list[str] | None = None,
    incremental_column: str | None = None,
    valid_from_column: str | None = None,
    valid_to_column: str | None = None,
    write_mode: str = "overwrite",
    format: str = "delta",
):
    """Create a definition for how to compute a blueprint.

    A blueprint is a function that takes any number of blueprints (or zero) and returns a dataframe.
    In addition, blueprint-information registered to know how to write the dataframe to a target table.

    Args:
        name (str): The name of the blueprint. If not provided, the name of the function will be used. The name must be unique across all blueprints.
        table_uri (str): The URI of the target table. If not provided, the blueprint will not be stored as a table.
        schema (pl.Schema, optional): The schema of the output dataframe. If provided, transformation function will be validated against this schema.
        primary_keys (list[str], optional): The primary keys of the target table. Is required for `upsert` and `scd2` write_mode.
        incremental_column (str, optional): The incremental column for the target table. Is required for `incremental` write mode.
        valid_from_column (str, optional): The name of the valid from column. Is required for `scd2` write mode.
        valid_to_column (str, optional): The name of the valid to column. Is required for `scd2` write mode.
        write_mode (str): The write method to use. Defaults to `overwrite`. Options are: `append`, `overwrite`, `upsert`, `incremental`, `replace_range`, and `scd2`.
        format (str): The format to use. Defaults to `delta`.

    Example:
        Creates a blueprint for the `silver_customer` table, which is derived from the `bronze_customer` table.
        The `bronze_customer` must be another blueprint.

        ```python
        from blueno import blueprint, Blueprint, DataFrameType

        @blueprint(
            table_uri="/path/to/silver/customer",
            primary_keys=["customer_id"],
            write_mode="overwrite",
        )
        def silver_customer(self: Blueprint, bronze_customer: DataFrameType) -> DataFrameType

            # Deduplicate customers
            df = bronze_customers.unique(subset=self.primary_keys)

            return df
        ```
    """
    _primary_keys = primary_keys or []

    if schema is not None and not isinstance(schema, pl.Schema):
        msg = "`schema` must be a polars schema (`pl.Schema`)."
        logger.error(msg)
        raise GenericBlueprintError(msg)

    if write_mode not in ["append", "overwrite", "upsert", "incremental", "replace_range", "scd2"]:
        msg = "`write_method` must be one of: 'append', 'overwrite', 'upsert', 'incremental', 'replace_range', 'scd2'."
        logger.error(msg)
        raise GenericBlueprintError(msg)

    if format not in ["delta"]:
        msg = f"`format` must be one of: 'delta'. Got {format}."
        logger.error(msg)
        raise GenericBlueprintError(msg)

    if write_mode == "upsert" and not primary_keys:
        msg = "`primary_keys` must be provided for `upsert` write mode."
        logger.error(msg)
        raise GenericBlueprintError(msg)

    if write_mode in ("incremental", "replace_range") and not incremental_column:
        msg = "`incremental_column` must be provided for `incremental` and `replace_range` write mode."
        logger.error(msg)
        raise GenericBlueprintError(msg)

    if write_mode == "scd2" and (not valid_from_column or not valid_to_column):
        msg = "`valid_from_column` and `valid_to_column` must be provided for `scd2` write mode."
        logger.error(msg)
        raise GenericBlueprintError(msg)

    if write_mode == "scd2" and not primary_keys:
        msg = "`primary_keys` must be provided for `scd2` write mode."
        logger.error(msg)
        raise GenericBlueprintError(msg)

    def decorator(func: types.FunctionType):
        _name = name or func.__name__

        blueprint = Blueprint(
            table_uri=table_uri,
            schema=schema,
            name=_name,
            primary_keys=_primary_keys,
            incremental_column=incremental_column,
            valid_from_column=valid_from_column,
            valid_to_column=valid_to_column,
            write_mode=write_mode,
            _transform_fn=func,
            format=format,
        )
        blueprint_registry.register(blueprint)

        return lambda: blueprint

    return decorator
