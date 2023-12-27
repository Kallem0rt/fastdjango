import logging
import os
from logging.config import dictConfig

from pydantic import BaseModel


def get_logger():
    dictConfig(LogConfig().dict())
    logging.getLogger().setLevel(logging.INFO)
    logger = logging.getLogger(os.getenv("NAME"))
    return logger


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = os.getenv("NAME")
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(funcName)20s() | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers: dict = {
        LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
    }
