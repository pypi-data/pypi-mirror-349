from importlib.metadata import PackageNotFoundError, version

from blueno.auth import (
    get_azure_storage_access_token,
    get_fabric_bearer_token,
    get_onelake_access_token,
)
from blueno.etl.types import DataFrameType

# from blueno.blueprint import (
#     Blueprint,
#     Task,
#     blueprint,
#     task,
# )
from blueno.orchestration.blueprint import Blueprint, blueprint
from blueno.orchestration.job import job_registry
from blueno.orchestration.pipeline import create_pipeline
from blueno.orchestration.task import Task, task

__all__ = (
    "get_fabric_bearer_token",
    "get_azure_storage_access_token",
    "get_onelake_access_token",
    "blueprint",
    "DataFrameType",
    "Blueprint",
    "task",
    "Task",
    "create_pipeline",
    "job_registry",
)


try:
    __version__ = version("blueno")
except PackageNotFoundError:
    # package is not installed
    __version__ = "0.0.0"
