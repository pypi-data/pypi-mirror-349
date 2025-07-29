import logging
from typing import Annotated, Literal, Optional

from cyclopts import App, Group, Parameter

from blueno.blueprint import blueprint_registry

logger = logging.getLogger(__name__)


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    _format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    # format = "%(asctime)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    # # FORMATS = {
    # #     logging.DEBUG: grey + format + reset,
    # #     logging.INFO: grey + format + reset,
    # #     logging.WARNING: yellow + format + reset,
    # #     logging.ERROR: red + format + reset,
    # #     logging.CRITICAL: bold_red + format + reset,
    # # }

    def format(self, record):
        # log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(self._format)
        return formatter.format(record)


app = App(default_parameter=Parameter(negative=()))
global_args = Group(
    name="Global arguments", default_parameter=Parameter(show_default=False, negative=())
)


@app.command
def run(
    project_dir: str,
    select: Optional[list[str]] = None,
    show_dag: bool = False,
    concurrency: int = 1,
    help: Annotated[bool, Parameter(group=global_args, help="Show this help and exit")] = False,
    log_level: Annotated[
        Literal["DEBUG", "INFO", "WARNING", "ERROR"],
        Parameter(group=global_args, help="Log level to use"),
    ] = "INFO",
):
    """
    Run the blueprints

    Args:
        project_dir (str): Path to the blueprints
        concurrency (int): Number of concurrent tasks to run
        select: List of blueprints to run. If not provided, all blueprints will be run
        show_dag: Whether to show the DAG of the blueprints

    """

    ch = logging.FileHandler("blueno.log")
    # ch = logging.StreamHandler()  # ty: ignore[no-matching-overload]
    ch.setLevel(log_level)
    ch.setFormatter(CustomFormatter())
    logging.basicConfig(
        level=log_level,
        handlers=[ch],
    )

    blueprint_registry.discover_blueprints(project_dir)
    blueprint_registry.validate_dependencies()

    if show_dag:
        blueprint_registry.render_dag()

    logger.info(f"Starting blueprint execution {concurrency} tasks at a time")
    blueprint_registry.run(subset=select, concurrency=concurrency)


@app.command
def run_remote(
    project_dir: str,
    workspace_id: str,
    lakehouse_id: str,
    notebook_id: str,
    select: Optional[list[str]] = None,
    concurrency: int = 1,
    v_cores: int = 2,
    help: Annotated[bool, Parameter(group=global_args, help="Show this help and exit")] = False,
    log_level: Annotated[
        Literal["DEBUG", "INFO", "WARNING", "ERROR"],
        Parameter(group=global_args, help="Log level to use"),
    ] = "INFO",
):
    """
    Run the blueprints in a Microsoft Fabric remote environment.
    It uploads the blueprints to the target lakehouse in a temporary folder, and runs the blueprints from a notebook.

    Args:
        project_dir (str): Path to the blueprints
        workspace_id (str): The workspace id to use
        lakehouse_id (str): The lakehouse id to use
        notebook_id (str): The notebook id to use
        concurrency (int): Number of concurrent tasks to run
        v_cores (int): Number of vCores to use
        select: List of blueprints to run. If not provided, all blueprints will be run

    https://app.powerbi.com/groups/a66707df-7616-41bb-a542-c7b0f70f4a5d/lakehouses/bf969d43-9b7a-4815-9a80-701afd5e5fb0?experience=power-bi
    https://app.powerbi.com/groups/a66707df-7616-41bb-a542-c7b0f70f4a5d/synapsenotebooks/368c6467-3a69-4c06-9799-f56dfb01241c?experience=power-bi
    """
    import uuid

    from blueno.fabric import (
        run_notebook,
        upload_folder_contents,
    )

    ch = logging.StreamHandler()  # ty: ignore[no-matching-overload]
    ch.setLevel(log_level)
    ch.setFormatter(CustomFormatter())
    logging.basicConfig(
        level=log_level,
        handlers=[ch],
    )

    blueprint_registry.discover_blueprints(project_dir)
    blueprint_registry.validate_dependencies()

    destination_folder = project_dir.split("/")[-1] + "_" + str(uuid.uuid4()).split("-")[0]

    upload_folder_contents(
        source_folder=project_dir,
        workspace_name="JSJ_AquaVilla",
        lakehouse_name="LH",
        destination_folder=destination_folder,
    )

    logger.info(f"Starting blueprint execution {concurrency} tasks at a time")

    execution_data = {
        "parameters": {
            "concurrency": {"value": concurrency, "type": "int"},
            "project_dir": {"value": destination_folder, "type": "string"},
            "log_level": {"value": log_level, "type": "string"},
            # "select": { "value": " ".join(select), "type": "string"},
        },
        "configuration": {
            "vCores": v_cores,
        },
    }

    run_notebook(workspace_id=workspace_id, notebook_id=notebook_id, execution_data=execution_data)


def main():
    app()


if __name__ == "__main__":
    main()
