import logging
import logging.config
import pathlib

from newby.loggers import ColoredFormatter

logging.config.fileConfig(
    str(pathlib.Path(__file__).parent.resolve()) + "/logging_config.ini"
)
logger = logging.getLogger()
