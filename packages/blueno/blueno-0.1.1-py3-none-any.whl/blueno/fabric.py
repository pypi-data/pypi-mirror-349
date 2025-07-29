import logging
import os
import shlex
import shutil
import subprocess
import sys
import time
from typing import Any

import requests

from blueno.auth import get_fabric_bearer_token

logger = logging.getLogger(__name__)


def paginated_get_request(endpoint: str, data_key: str) -> list[dict[str, Any]]:
    """
    Retrieves paginated data from the specified API endpoint.

    This function makes repeated GET requests to the specified endpoint of the
    Fabric REST API, handling pagination automatically. It uses a bearer token
    for authentication and retrieves data from each page, appending the results
    to a list. Pagination continues until no `continuationToken` is returned.

    Args:
        endpoint (str): The API endpoint to retrieve data from.
        data_key (str): The key in the response JSON that contains the list of data to be returned.

    Returns:
        A list of dictionaries containing the data from all pages.

    Raises:
        requests.exceptions.RequestException: If the HTTP request fails or returns an error.
    """
    base_url = "https://api.fabric.microsoft.com/v1"
    token = get_fabric_bearer_token()
    headers = {"Authorization": f"Bearer {token}"}

    responses = []
    continuation_token = None
    while True:
        params = {"continuationToken": continuation_token} if continuation_token else {}

        response = requests.get(f"{base_url}/{endpoint}", headers=headers, params=params)
        response.raise_for_status()
        data: dict = response.json()

        responses.extend(data.get(data_key))

        continuation_token = data.get("continuationToken")
        if not continuation_token:
            break

    return responses


def get_item_from_paginated_get_request(
    endpoint: str, data_key: str, item_key: str, item_value: str
) -> dict[str, Any]:
    """
    Recursively paginates the API endpoint until specified item is found and returns it.

    This function makes repeated GET requests to the specified endpoint of the
    Fabric REST API, handling pagination automatically. It uses a bearer token
    for authentication and retrieves data from each page, appending the results
    to a list. Pagination continues until the specified item is found or no
    `continuationToken` is returned.

    Args:
        endpoint (str): The API endpoint to retrieve data from.
        data_key (str): The key in the response JSON that contains the list of data to be returned.
        item_key (str): The key in the data dictionary that contains the item to be returned.
        item_value (str): The value of the item to be returned.

    Returns:
        A dictionary containing the item to be returned.

    Raises:
        requests.exceptions.RequestException: If the HTTP request fails or returns an error.
        ValueError: If the item is not found.
    """
    base_url = "https://api.fabric.microsoft.com/v1"
    token = get_fabric_bearer_token()
    headers = {"Authorization": f"Bearer {token}"}

    continuation_token = None
    while True:
        params = {"continuationToken": continuation_token} if continuation_token else {}

        response = requests.get(f"{base_url}/{endpoint}", headers=headers, params=params)
        response.raise_for_status()
        data: dict = response.json()

        for item in data.get(data_key):
            if item.get(item_key) == item_value:
                return item

        continuation_token = data.get("continuationToken")
        if not continuation_token:
            break

    raise ValueError(f"Item with {item_key} {item_value} not found")


def get_request(endpoint: str, content_only: bool = True) -> requests.Response | dict[str, Any]:
    """
    Retrieves data from a specified API endpoint.

    This function makes a GET request to the specified endpoint of the Azure Fabric API,
    using a bearer token for authentication. It returns the JSON response as a list of
    dictionaries containing the data returned by the API.

    Args:
        endpoint (str): The API endpoint to send the GET request to.
        content_only (bool): Whether to return the content of the response only.

    Returns:
        A list of dictionaries containing the data returned from the API or the response object.

    Raises:
        requests.exceptions.RequestException: If the HTTP request fails or returns an error.
    """
    base_url = "https://api.fabric.microsoft.com/v1"
    token = get_fabric_bearer_token()
    headers = {"Authorization": f"Bearer {token}"}
    params = {}

    response = requests.get(f"{base_url}/{endpoint}", headers=headers, params=params)

    if content_only:
        if response.status_code >= 400:
            logger.error(
                f"Request failed with status code {response.status_code}: {response.content}"
            )
        response.raise_for_status()
        return response.json()

    return response


def post_request(
    endpoint: str, data: dict[str, str], content_only: bool = True
) -> requests.Response | dict[str, Any]:
    """
    Sends a POST request to a specified API endpoint.

    This function makes a POST request to the specified endpoint of the Azure Fabric API,
    using a bearer token for authentication. It sends the provided data in JSON format
    and returns either the JSON response or the full response object.

    Args:
        endpoint (str): The API endpoint to send the POST request to.
        data (dict[str, str]): The data to be sent in the request body.
        content_only (bool): Whether to return the content of the response only.

    Returns:
        Either the JSON response as a dictionary or the full response object.

    Raises:
        requests.exceptions.RequestException: If the HTTP request fails or returns an error.
    """
    base_url = "https://api.fabric.microsoft.com/v1"
    token = get_fabric_bearer_token()
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(f"{base_url}/{endpoint}", headers=headers, json=data)

    if content_only:
        if response.status_code >= 400:
            logger.error(
                f"Request failed with status code {response.status_code}: {response.json()}"
            )
        response.raise_for_status()
        return response.json()

    return response


def patch_request(
    endpoint: str, data: dict[str, str], content_only: bool = True
) -> requests.Response | dict[str, Any]:
    """
    Sends a PATCH request to a specified API endpoint.

    This function makes a PATCH request to the specified endpoint of the Azure Fabric API,
    using a bearer token for authentication. It sends the provided data in JSON format
    and returns either the JSON response or the full response object.

    Args:
        endpoint (str): The API endpoint to send the PATCH request to.
        data (dict[str, str]): The data to be sent in the request body.
        content_only (bool): Whether to return the content of the response only.

    Returns:
        Either the JSON response as a dictionary or the full response object.

    Raises:
        requests.exceptions.RequestException: If the HTTP request fails or returns an error.
    """
    base_url = "https://api.fabric.microsoft.com/v1"
    token = get_fabric_bearer_token()
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.patch(f"{base_url}/{endpoint}", headers=headers, json=data)

    if content_only:
        if response.status_code >= 400:
            logger.error(
                f"Request failed with status code {response.status_code}: {response.json()}"
            )
        response.raise_for_status()
        return response.json()

    return response


def delete_request(endpoint: str) -> requests.Response:
    """
    Sends a DELETE request to a specified API endpoint.

    This function makes a DELETE request to the specified endpoint of the Azure Fabric API,
    using a bearer token for authentication.

    Args:
        endpoint (str): The API endpoint to send the DELETE request to.

    Returns:
        The response object from the DELETE request.

    Raises:
        requests.exceptions.RequestException: If the HTTP request fails or returns an error.
    """
    base_url = "https://api.fabric.microsoft.com/v1"
    token = get_fabric_bearer_token()
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.delete(f"{base_url}/{endpoint}", headers=headers)
    if response.status_code >= 400:
        logger.error(f"Request failed with status code {response.status_code}: {response.json()}")
    response.raise_for_status()
    return response


def run_pipeline(
    workspace_id: str,
    pipeline_id: str,
    parameters: dict[str, Any] | None = None,
    poll_interval: float = 5.0,
    timeout: float = 5 * 60.0,
) -> requests.Response:
    """
    Runs a notebook in the specified workspace.

    Args:
        workspace_id (str): The ID of the workspace where the pipeline is located.
        pipeline_id (str): The ID of the pipeline to run.
        parameters (dict[str, Any], optional): Parameters to pass to the pipeline. Defaults to None.
        poll_interval (float): The interval in seconds to poll the pipeline status. Defaults to 5.0.
        timeout (float): The maximum time in seconds to wait for the pipeline to complete. Defaults to 300.0.

    Returns:
        The response object from the POST request.

    Raises:
        requests.exceptions.RequestException: If the HTTP request fails or returns an error.
    """
    base_url = "https://api.fabric.microsoft.com/v1"
    token = get_fabric_bearer_token()
    headers = {"Authorization": f"Bearer {token}"}

    data = {
        "executionData": {
            "parameters": parameters or {},
        }
    }
    logger.info(
        f"Running pipeline {pipeline_id} in workspace {workspace_id} with parameters: {parameters}"
    )

    response = requests.post(
        f"{base_url}/workspaces/{workspace_id}/items/{pipeline_id}/jobs/instances?jobType=Pipeline",
        headers=headers,
        json=data,
    )
    if response.status_code >= 400:
        logger.error(f"Request failed with status code {response.status_code}: {response.json()}")
    response.raise_for_status()

    url = response.headers.get("Location")

    time_elapsed = 0
    while True:
        time.sleep(5)  # Wait for 5 seconds before checking the status
        response = requests.get(url, headers=headers)

        if response.status_code >= 400:
            logger.error(
                f"Request failed with status code {response.status_code}: {response.json()}"
            )
            break
        response.raise_for_status()

        if response.json().get("status") in ("Completed", "Failed"):
            logger.info(
                f"Pipeline {pipeline_id} in workspace {workspace_id} completed successfully."
            )
            break

        time_elapsed += poll_interval
        if time_elapsed >= timeout:
            logger.warning(
                f"Polling the pipeline status of {pipeline_id} in workspace {workspace_id} exceeded the timeout limit after {timeout} seconds. This does not necessarily mean the pipeline failed."
            )
            break

        # Else we should be InProgress
        logger.info(
            f"Pipeline {pipeline_id} in workspace {workspace_id} is still running. Status: {response.json().get('status')}"
        )

    return response


def run_notebook(
    notebook_id: str,
    workspace_id: str,
    execution_data: dict[str, Any] | None = None,
    poll_interval: float = 5.0,
    timeout: float = 5 * 60.0,
) -> requests.Response:
    """
    Runs a notebook in the specified workspace.

    Args:
        notebook_id (str): The ID of the notebook to run.
        workspace_id (str): The ID of the workspace where and notebook is located.
        execution_data (dict[str, Any], optional): Execution data to pass to the notebook. Defaults to None.
        poll_interval (float): The interval in seconds to poll the pipeline status. Defaults to 5.0.
        timeout (float): The maximum time in seconds to wait for the pipeline to complete. Defaults to 300.0.

    Returns:
        The response object from the POST request.

    Raises:
        requests.exceptions.RequestException: If the HTTP request fails or returns an error.
    """
    base_url = "https://api.fabric.microsoft.com/v1"
    token = get_fabric_bearer_token()
    headers = {"Authorization": f"Bearer {token}"}

    data = {
        "executionData": execution_data or {},
    }
    logger.info(
        f"Running notebook {notebook_id} in workspace {workspace_id} with parameters: {execution_data}"
    )

    response = requests.post(
        f"{base_url}/workspaces/{workspace_id}/items/{notebook_id}/jobs/instances?jobType=RunNotebook",
        headers=headers,
        json=data,
    )
    if response.status_code >= 400:
        logger.error(f"Request failed with status code {response.status_code}: {response.json()}")
    response.raise_for_status()

    url = response.headers.get("Location")

    time_elapsed = 0
    while True:
        time.sleep(5)  # Wait for 5 seconds before checking the status
        response = requests.get(url, headers=headers)

        if response.status_code >= 400:
            logger.error(
                f"Request failed with status code {response.status_code}: {response.json()}"
            )
            break
        response.raise_for_status()

        if response.json().get("status") == "Completed":
            logger.info(
                f"Notebook {notebook_id} in workspace {workspace_id} completed successfully."
            )
            break

        if response.json().get("status") == "Failed":
            logger.info(f"Notebook {notebook_id} in workspace {workspace_id} failed.")
            logger.error(
                f"Notebook {notebook_id} in workspace {workspace_id} failed with error: {response.json()}"
            )
            break

        time_elapsed += poll_interval
        if time_elapsed >= timeout:
            logger.warning(
                f"Polling the notebook status of {notebook_id} in workspace {workspace_id} exceeded the timeout limit after {timeout} seconds. This does not necessarily mean the pipeline failed."
            )
            break

        # Else we should be InProgress
        logger.info(
            f"Notebook {notebook_id} in workspace {workspace_id} is still running. Status: {response.json().get('status')}"
        )

    return response


def upload_folder_contents(
    workspace_name: str, lakehouse_name: str, source_folder: str, destination_folder: str
) -> None:
    """
    Uploads the contents of a local folder to a specified destination folder in OneLake using AzCopy.
    Based on: https://medium.com/microsoftazure/ingest-data-into-microsoft-onelake-using-azcopy-a6e0e199feee

    Args:
        source_folder (str): The path to the local folder to upload.
        destination_folder (str): The destination folder in OneLake where the contents will be uploaded.

    Raises:
        requests.exceptions.RequestException: If the HTTP request fails or returns an error.
    """

    # Check if AzCopy is installed
    if not shutil.which("azcopy"):
        logger.error(
            "AzCopy is not installed. Please install it from https://learn.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-v10"
        )
        sys.exit(1)

    # Check if the source folder exists
    if not os.path.exists(source_folder):
        logger.error(f"Source folder {source_folder} does not exist.")
        sys.exit(1)

    cmds = [
        "azcopy",
        "copy",
        f"{source_folder}/*",
        f"https://onelake.blob.fabric.microsoft.com/{workspace_name}/{lakehouse_name}.Lakehouse/Files/{destination_folder}/",
        # "--overwrite=prompt",
        "--from-to=LocalBlob",
        # "--delete-destination=true",
        "--blob-type=BlockBlob",
        "--follow-symlinks",
        "--check-length=true",
        "--put-md5",
        "--disable-auto-decoding=false",
        "--recursive",
        "--trusted-microsoft-suffixes=onelake.blob.fabric.microsoft.com",
        "--log-level=INFO",
    ]
    logger.info(f"Uploading {source_folder} to {destination_folder} in OneLake using AzCopy")

    # Run the AzCopy command
    try:
        cmd = shlex.join(cmds)
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True)
        print(f"AzCopy command output: {result.stdout.decode()}")
        logger.info(f"AzCopy command output: {result.stdout.decode()}")
    except subprocess.CalledProcessError as e:
        logger.error(f"AzCopy command failed with error:\n{e.stderr.decode()}\n{e.stdout.decode()}")
        sys.exit(1)


def remove_folder_contents(workspace_name: str, lakehouse_name: str, folder: str) -> None:
    """
    Uploads the contents of a local folder to a specified destination folder in OneLake using AzCopy.
    Based on: https://medium.com/microsoftazure/ingest-data-into-microsoft-onelake-using-azcopy-a6e0e199feee

    Args:
        source_folder (str): The path to the local folder to upload.
        destination_folder (str): The destination folder in OneLake where the contents will be uploaded.

    Raises:
        requests.exceptions.RequestException: If the HTTP request fails or returns an error.
    """

    # Check if AzCopy is installed
    if not shutil.which("azcopy"):
        logger.error(
            "AzCopy is not installed. Please install it from https://learn.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-v10"
        )
        sys.exit(1)

    cmds = [
        "azcopy",
        "remove",
        f"https://onelake.blob.fabric.microsoft.com/{workspace_name}/{lakehouse_name}.Lakehouse/Files/{folder}/",
        # "--overwrite=prompt",
        # "--from-to=LocalBlob",
        # "--delete-destination=true",
        # "--blob-type=BlockBlob",
        # "--follow-symlinks",
        # "--check-length=true",
        # "--put-md5",
        # "--disable-auto-decoding=false",
        "--recursive",
        "--permanent-delete=SnapshotsAndVersions",
        "--trusted-microsoft-suffixes=onelake.blob.fabric.microsoft.com",
        "--log-level=INFO",
    ]
    logger.info(f"Deleting {folder} in OneLake using AzCopy")

    # Run the AzCopy command
    try:
        cmd = shlex.join(cmds)
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True)
        print(f"AzCopy command output: {result.stdout.decode()}")
        logger.info(f"AzCopy command output: {result.stdout.decode()}")
    except subprocess.CalledProcessError as e:
        logger.error(f"AzCopy command failed with error:\n{e.stderr.decode()}\n{e.stdout.decode()}")
        sys.exit(1)
