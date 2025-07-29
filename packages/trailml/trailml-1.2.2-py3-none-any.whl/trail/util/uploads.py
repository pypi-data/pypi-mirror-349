import hashlib
import os
import sys
from enum import Enum
from pathlib import Path

import requests
import sentry_sdk
from gql.transport.exceptions import TransportQueryError
from requests import RequestException
from tqdm import tqdm

from trail.exception.trail import RemoteTrailException, TrailUnavailableException
from trail.exception.upload import UploadError
from trail.libconfig import is_development_environment
from trail.userconfig import userconfig
from trail.util.gql_client import build_gql_client

SUPPORTED_FILE_EXTENSIONS = (".py", ".ipynb", ".txt", ".yml", ".yaml")


class NebulaTaskType(Enum):
    CHUNK_EMBEDDING = "chunk_embedding"
    ARTIFACT_CONTEXT_INDEXING = "artifact_context_fetching"
    ARTIFACT_CONTENT_EMBEDDING = "artifact_embedding"
    JUPYTER_NOTEBOOK_CELL_CONTENT_EMBEDDING = "jupyter_notebook_cell_content_embedding"
    JUPYTER_NOTEBOOK_CELL_OUTPUT_INDEXING = "jupyter_notebook_cell_output_indexing"


ADD_SOURCE_FILES_MUTATION = """
     mutation AddSourceFiles($projectId: String!,
      $files: [SourceFileInput!]!,
       $experimentId: String!) {
         addSourceFiles(projectId: $projectId, files: $files, experimentId: $experimentId) {
             sourceFiles {
                 id
                 fileName
                 filePath
                 fileHash
                 creationTimestamp
                 lastUpdatedAt
             }
             presignedUrls
         }
     }
 """


def upload_file(
    local_file_path: str, is_absolute_path=False, parent_directory="", tasks=None
):
    """Uploads a file to Trail.

    Args:
        local_file_path (str): The path to the local file to be uploaded.
        is_absolute_path (bool, optional): Indicates whether the local_file_path is an absolute
                                           path. Defaults to False.
        parent_directory (str, optional): The absolute path of the file. Required if
                                          is_absolute_path is False. Defaults to "".
        tasks (List[GrapheneNebulaTaskType], optional): List of tasks associated with the file.

    Raises:
        UploadError: If the upload fails.
    """
    if not is_absolute_path:
        project_directory = os.path.dirname(parent_directory)
        local_file_path = os.path.abspath(
            os.path.join(project_directory, local_file_path)
        )

    signed_url = _register_files(
        project_id=userconfig().project().config["id"],
        experiment_id=userconfig().project().parent_experiment_id,
        files=[
            {
                "fileName": os.path.basename(local_file_path),
                "filePath": _get_path_relative_to_config(local_file_path),
                "fileHash": _calculate_file_hash(local_file_path),
                "tasks": tasks if tasks else [],
            }
        ],
    )[0]

    try:
        with open(local_file_path, "rb") as local_file:
            response = requests.put(signed_url, data=local_file, allow_redirects=False)

        response.raise_for_status()
    except RequestException as e:
        raise UploadError(local_file_path) from e


def upload_folder(local_folder: str) -> bool:
    """Uploads files within a specified folder and its subfolders.

    Args:
        local_folder (str): The path to the local folder containing files to be uploaded.

    Raises:
        FileNotFoundError: If the specified directory does not exist.
        UploadError: If any file upload within the folder fails.

    Returns:
        bool: True if the upload is successful, False if the folder is empty.
    """
    print(f"Uploading folder {local_folder}")

    project_directory = os.getcwd()
    full_local_folder = os.path.abspath(os.path.join(project_directory, local_folder))

    if not os.path.isdir(full_local_folder):
        raise FileNotFoundError(f"Directory {full_local_folder} does not exist.")

    if not os.listdir(full_local_folder):
        return False

    files_to_upload = [
        os.path.join(root, file)
        for root, _, files in os.walk(full_local_folder)
        for file in files
        if file.endswith(SUPPORTED_FILE_EXTENSIONS)
    ]

    for filepath in tqdm(files_to_upload):
        upload_file(
            local_file_path=filepath,
            is_absolute_path=True,
        )

    return True


def _register_files(project_id: str, experiment_id: str, files: list) -> list[str]:
    """Call the GraphQL mutation to add source files and return the presigned URLs
    for direct file upload to GCP

    Args:
        project_id (str): The ID of the project.
        experiment_id (str): The ID of the experiment.
        files (list): A list of dictionaries containing file details.
    """
    variables = {
        "projectId": project_id,
        "files": files,
        "experimentId": experiment_id,
    }
    client = build_gql_client()
    try:
        response = client.execute(
            query=ADD_SOURCE_FILES_MUTATION,
            variable_values=variables,
        )
        return response["addSourceFiles"]["presignedUrls"]

    except TransportQueryError as e:
        if is_development_environment():
            raise RemoteTrailException("Could not register files in terra") from e
        else:
            sentry_sdk.capture_exception(e)
            print(TrailUnavailableException().message, file=sys.stderr)


def _calculate_file_hash(file_path):
    """Calculate the hash of a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The hash of the file.
    """
    BUF_SIZE = 65536  # Read in 64kb chunks
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha256.update(data)

    return sha256.hexdigest()


def _get_path_relative_to_config(file_path) -> str:
    file_path = Path(file_path)
    config_parent = Path(os.path.abspath(userconfig().path)).parent

    try:
        relative_path = file_path.relative_to(config_parent)
        return str(config_parent.name / relative_path)
    except ValueError:
        raise ValueError("File is not a located within the project directory.")
