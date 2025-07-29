import os

from trail.libconfig import libconfig


def find_config_file_in_directory_hierarchy():
    current_dir = libconfig.TRAIL_CONFIG_PATH

    while True:
        file_path = os.path.join(current_dir, libconfig.PRIMARY_USER_CONFIG_PATH)

        if os.path.isfile(file_path):
            return file_path

        parent_dir = os.path.dirname(current_dir)

        if current_dir == parent_dir:
            break

        current_dir = parent_dir

    raise FileNotFoundError(
        "No config file found in the directory hierarchy; this likely indicates you are not in a trail project directory."
    )
