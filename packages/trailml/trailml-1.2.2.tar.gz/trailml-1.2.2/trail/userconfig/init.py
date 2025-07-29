import os

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportQueryError

from trail.exception.trail import TrailUnavailableException
from trail.libconfig import libconfig
from trail.userconfig import MainConfig
from trail.util import auth

FETCH_ALL_PROJECTS = """
    query {
        allProjects {
            id
            title
            mostRecentExperiment {
                id
            }
        }
    }
"""


def get_user_credentials():
    email = input("Email: ")
    api_key = input("API Key: ")
    return email, api_key


def get_endpoint_url():
    url = input("Overwrite Trail Endpoint URL (optional, press Enter to skip): ")
    return url if url else ""


def get_project_data(auth_header: dict, user_specified_endpoint_url: str) -> dict:
    """Get data for all projects.

    Returns:
        dict: Dictionary of projects with project IDs as keys
    """
    try:
        transport = AIOHTTPTransport(
            libconfig.gql_endpoint_url(user_specified_endpoint_url), headers=auth_header
        )
        client = Client(transport=transport)
        result = client.execute(document=gql(FETCH_ALL_PROJECTS))
        return {project["id"]: project for project in result["allProjects"]}
    except TransportQueryError as e:
        raise TrailUnavailableException() from e


def select_project(
    auth_header: dict, user_specified_endpoint_url: str
) -> tuple[str, dict]:
    """Select a project interactively from the available projects."""
    projects = get_project_data(auth_header, user_specified_endpoint_url)

    print("\nYour projects are listed below:\n")
    print("Project ID | Project Title")
    for project in sorted(projects.values(), key=lambda x: x["id"]):
        print(f"{project['id']}     | {project['title']}")

    while True:
        project_id = input("\nSelect a project ID: ")
        if project_id in projects:
            return project_id, projects[project_id]


def select_experiment(project_data: dict) -> str:
    """Select an experiment ID, with the most recent experiment as default."""
    default_experiment_id = project_data.get("mostRecentExperiment", {}).get(
        "id", "N/A"
    )
    parent_experiment_id = input(
        f"\nSelect a parent experiment ID (Default: {default_experiment_id}): "
    )
    return parent_experiment_id if parent_experiment_id else default_experiment_id


def select_project_and_parent_experiment(
    auth_header: dict, user_specified_endpoint_url: str
):
    """Combined function for backward compatibility."""
    project_id, project_data = select_project(auth_header, user_specified_endpoint_url)
    experiment_id = select_experiment(project_data)
    return project_id, experiment_id


def update_config_project(config: MainConfig, project_id: str):
    """Update only the project ID in the config."""
    config.config["projects"]["id"] = project_id
    config.save()


def update_config_experiment(config: MainConfig, experiment_id: str):
    """Update only the experiment ID in the config."""
    config.config["projects"]["parentExperimentId"] = experiment_id
    config.save()


def create_config(email, api_key, project_id, parent_experiment_id, endpoint_url):
    """Create a new config file with all settings."""
    config = MainConfig(
        os.path.join(os.getcwd(), libconfig.PRIMARY_USER_CONFIG_PATH),
        {
            "endpointUrl": endpoint_url,
            "email": email,
            "apiKey": api_key,
            "projects": {"id": project_id, "parentExperimentId": parent_experiment_id},
        },
    )
    config.save()


def init_environment():
    print(f"Don't have an account yet? Sign up here: {libconfig.TRAIL_SIGN_UP_URL}\n")
    print(
        "Your configuration file will be stored in the current directory. "
        "Make sure that you are in the root directory of your project."
    )

    email, api_key = get_user_credentials()
    endpoint_url = get_endpoint_url()
    auth_header = auth.build_auth_header(email=email, api_key=api_key)

    project_id, project_data = select_project(auth_header, endpoint_url)
    parent_experiment_id = select_experiment(project_data)

    create_config(email, api_key, project_id, parent_experiment_id, endpoint_url)
    print("Initialization completed.")
