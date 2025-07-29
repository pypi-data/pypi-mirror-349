import os

from trail.libconfig import libconfig
from trail.userconfig.config import MainConfig
from trail.userconfig.init import init_environment

_userconfig = None


def userconfig():
    global _userconfig

    if not _userconfig:
        primary_config_path = os.path.join(
            libconfig.TRAIL_CONFIG_PATH, libconfig.PRIMARY_USER_CONFIG_PATH
        )
        if os.path.isfile(primary_config_path):
            _userconfig = MainConfig.from_file(primary_config_path)
        else:
            # initialize environment
            init_environment()

            return userconfig()

    return _userconfig
