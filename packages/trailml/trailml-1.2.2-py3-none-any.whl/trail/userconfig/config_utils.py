import os
from typing import Optional

from trail.userconfig.config import MainConfig
from trail.util import auth
from trail.userconfig.init import (
    select_project,
    select_experiment,
    update_config_project,
    update_config_experiment,
    get_project_data,
)
from trail import libconfig


def _get_config() -> MainConfig:
    """Helper to get the config from the standard location"""
    config_path = os.path.join(
        libconfig.libconfig.TRAIL_CONFIG_PATH,
        libconfig.libconfig.PRIMARY_USER_CONFIG_PATH,
    )
    return MainConfig.from_file(config_path)


def set_project(project_id: Optional[str] = None, *, interactive: bool = True) -> str:
    """Set the current project ID in the trail configuration.

    Args:
        project_id: The project ID to set. If None and interactive=True, will trigger selection.
        interactive: Whether to allow interactive selection when project_id is None.

    Returns:
        The selected/set project ID
    """
    config = _get_config()
    auth_header = auth.build_auth_header(
        email=config.config["email"], api_key=config.config["apiKey"]
    )

    if project_id is None:
        if not interactive:
            raise ValueError("project_id must be provided when interactive=False")
        project_id, _ = select_project(
            auth_header, config.config.get("endpointUrl", "")
        )

    # Validate project exists
    projects = get_project_data(auth_header, config.config.get("endpointUrl", ""))
    if project_id not in projects:
        raise ValueError(f"Project {project_id} not found. Please set a valid project.")

    update_config_project(config, project_id)

    # After project is set, automatically trigger experiment selection if interactive
    if interactive:
        experiment_id = select_experiment(projects[project_id])
        update_config_experiment(config, experiment_id)

    return project_id


def set_experiment(
    experiment_id: Optional[str] = None, *, interactive: bool = True
) -> str:
    """Set the current experiment ID in the trail configuration.

    Args:
        experiment_id: The experiment ID to set. If None and interactive=True, will trigger selection.
        interactive: Whether to allow interactive selection when experiment_id is None.

    Returns:
        The selected/set experiment ID
    """
    config = _get_config()

    if experiment_id is None:
        if not interactive:
            raise ValueError("experiment_id must be provided when interactive=False")

        auth_header = auth.build_auth_header(
            email=config.config["email"], api_key=config.config["apiKey"]
        )

        projects = get_project_data(auth_header, config.config.get("endpointUrl", ""))
        current_project_id = config.config["projects"]["id"]

        if current_project_id not in projects:
            raise ValueError(
                f"Current project {current_project_id} not found. Please set a valid project first."
            )

        experiment_id = select_experiment(projects[current_project_id])

    update_config_experiment(config, experiment_id)
    return experiment_id
