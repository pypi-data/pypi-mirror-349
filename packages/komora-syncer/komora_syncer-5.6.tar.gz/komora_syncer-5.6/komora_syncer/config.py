import os
import sys

import appdirs
import yaml
from loguru import logger

from komora_syncer import __appname__

os.environ["XDG_CONFIG_DIRS"] = "/etc"
CONFIG_DIRS = (
    appdirs.user_config_dir(__appname__),
    appdirs.site_config_dir(__appname__),
)
CONFIG_FILENAME = "config.yml"


def get_config():
    """
    Get config file and load it with yaml
    :returns: loaded config in yaml, as a dict object
    """

    if getattr(get_config, "cache", None):
        return get_config.cache

    if os.environ.get("CONFIG_FOLDER_PATH"):
        config_path = os.path.join(os.environ.get("CONFIG_FOLDER_PATH"), CONFIG_FILENAME)
    else:
        for d in CONFIG_DIRS:
            config_path = os.path.join(d, CONFIG_FILENAME)
            if os.path.isfile(config_path):
                break
        else:
            logger.error(
                "No configuration file can be found. Please create a "
                "config.yml in one of these directories:\n"
                "{}".format(", ".join(CONFIG_DIRS))
            )
            exit(0)

    try:
        with open(config_path, "r") as config_file:
            conf = yaml.safe_load(config_file)
            get_config.cache = conf
            return conf
    except FileNotFoundError as e:
        logger.error(e)
        exit(0)


def configure_logger():
    logging_config = get_config().get("logging", {})
    level = logging_config.get("LOG_LEVEL", "DEBUG")

    logger.remove()

    # Add console sink (stdout) with formatting and level filtering
    logger.add(sys.stdout, level=level)
