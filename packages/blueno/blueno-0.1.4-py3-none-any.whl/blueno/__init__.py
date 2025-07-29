from importlib.metadata import PackageNotFoundError, version

from blueno.auth import (
    get_azure_storage_access_token,
    get_fabric_bearer_token,
    get_onelake_access_token,
)
from blueno.blueprint import (
    Blueprint,
    blueprint,
)
from blueno.etl.types import DataFrameType

__all__ = (
    "get_fabric_bearer_token",
    "get_azure_storage_access_token",
    "get_onelake_access_token",
    "blueprint",
    "DataFrameType",
    "Blueprint",
)


try:
    __version__ = version("blueno")
except PackageNotFoundError:
    # package is not installed
    __version__ = "0.0.0"
