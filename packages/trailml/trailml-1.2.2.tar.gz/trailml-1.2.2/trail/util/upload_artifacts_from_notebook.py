import base64

import nbformat
from gql import gql, Client

from trail.userconfig import userconfig
from trail.util.gql_client import build_gql_client

PUT_ARTIFACT_MUTATION = gql(
    """
    mutation (
        $experimentId: String!,
        $name: String!,
        $base64Data: String!,
        $tags: [String!],
        $callSiteKey: String,
    ) {
        putArtifact(
            experimentId: $experimentId,
            name: $name,
            base64Data: $base64Data,
            tags: $tags,
            callSiteKey: $callSiteKey
        ) {
            artifact {
                id
                name
                contentType
                size
                tags
                callSiteKey
            }
        }
    }
"""
)


def _save_cell_output_to_gql(
    output, cell_index: int, output_index: int, experiment_id: str, gql_client: Client
):
    file_name = ""
    base64_data = ""
    if output["output_type"] == "execute_result":
        if "text/html" in output["data"]:
            content = output["data"]["text/html"]
            file_name = f"output_{cell_index}_{output_index}.html"
            base64_data = base64.b64encode(content.encode()).decode()
    elif output["output_type"] == "display_data":
        if "image/png" in output["data"]:
            content = output["data"]["image/png"]
            file_name = f"output_{cell_index}_{output_index}.png"
            base64_data = content  # Already base64 encoded
    elif output["output_type"] == "stream":
        content = "".join(output["text"])
        file_name = f"output_{cell_index}_{output_index}.txt"
        base64_data = base64.b64encode(content.encode()).decode()

    if file_name and base64_data:
        gql_client.execute(
            PUT_ARTIFACT_MUTATION,
            variable_values={
                "experimentId": experiment_id,
                "name": file_name,
                "base64Data": base64_data,
                "tags": [],
                "callSiteKey": file_name,
            },
        )
    return file_name


def _read_notebook(file_path: str) -> nbformat.NotebookNode:
    """Read a Jupyter notebook and return its content."""
    with open(file_path) as f:
        return nbformat.read(f, as_version=4)


def _process_notebook_cells(
    notebook: nbformat.NotebookNode, gql_client: Client, experiment_id: str
) -> [str]:
    artifact_names = []
    for i, cell in enumerate(notebook["cells"]):
        if cell["cell_type"] == "code":
            stream_output_content = ""
            stream_output_index = -1

            for j, output in enumerate(cell.get("outputs", [])):
                if output["output_type"] == "stream":
                    # Aggregate stream outputs
                    stream_output_content += "".join(output["text"])
                    if stream_output_index == -1:
                        stream_output_index = j
                else:
                    # Process non-stream outputs immediately
                    artifact_name = _save_cell_output_to_gql(
                        output, i, j, experiment_id, gql_client
                    )
                    if artifact_name:
                        artifact_names.append(artifact_name)

            if stream_output_content:
                artifact_name = _save_cell_output_to_gql(
                    {"output_type": "stream", "text": [stream_output_content]},
                    i,
                    stream_output_index,
                    experiment_id,
                    gql_client,
                )
                if artifact_name:
                    artifact_names.append(artifact_name)

    return artifact_names


def upload_artifacts_from_notebook(file_name: str):
    client = build_gql_client()
    notebook = _read_notebook(file_name)
    experiment_id = userconfig().project().parent_experiment_id
    artifact_outputs = _process_notebook_cells(notebook, client, experiment_id)
    print(artifact_outputs)
