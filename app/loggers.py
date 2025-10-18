import logging

from app.core.config import settings

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "default": {
            "level": settings.LOG_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["default"],
            "level": settings.LOG_LEVEL,
        },
        "uvicorn": {
            "handlers": ["default"],
            "level": settings.LOG_LEVEL,
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["default"],
            "level": settings.LOG_LEVEL,
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["default"],
            "level": settings.LOG_LEVEL,
            "propagate": False,
        },
        "sqlalchemy.engine.Engine": {
            "level": settings.SQL_LOG_LEVEL,
            "handlers": ["default"],
            "propagate": False,
        },
        "sqlalchemy.pool": {
            "level": settings.SQL_LOG_LEVEL,
            "handlers": ["default"],
            "propagate": False,
        },
        "sqlalchemy.dialects": {
            "level": settings.SQL_LOG_LEVEL,
            "handlers": ["default"],
            "propagate": False,
        },
    },
}

