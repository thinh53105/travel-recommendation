from logging.config import dictConfig
import logging
from .config import config

dictConfig(config.logging.model_dump())
logger = logging.getLogger(config.logging.LOGGER_NAME)
