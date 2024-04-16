import os
import yaml
import logging.config

from config import Settings

settings = Settings()
path_res = settings.PATH_RES


def setup_logging(default_path=os.path.join(path_res, 'logging.yml'),
                  default_level=logging.INFO,
                  env_key='LOG_CFG'):
    """
    Setup logging configuration.

    Parameters
    ----------
    default_path : str
        logger configuration file path

    default_level : int
        default configuration of the root logger level.

    env_key : str
        environment variable key for logger configuration file path
    """

    try:
        os.mkdir(os.path.join(os.getcwd(), 'logs'))
    except FileExistsError:
        pass

    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
