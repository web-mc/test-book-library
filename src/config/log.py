import logging

from .config import app_config


class ErrorFilter(logging.Filter):
    def filter(self, record) -> bool:
        if record.levelno >= logging.ERROR:
            return True
        return False


class InfoFilter(logging.Filter):
    def filter(self, record) -> bool:
        if record.levelno <= logging.WARNING:
            return True
        return False


LOGGERS = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {
        "level": logging.INFO,
        "handlers": ["error_file", "info_file"],
    },
    "handlers": {
        # "console": {
        #     "level": logging.INFO,
        #     "class": "logging.StreamHandler",
        #     "formatter": "default",
        #     "stream": "ext://sys.stdout",
        # },
        "error_file": {
            "level": logging.ERROR,
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": app_config.log_dir / "errors.log",
            "mode": "a+",
            "backupCount": 3,
            "maxBytes": 5_000_000,
            "encoding": "utf-8",
            "filters": ["error_filter"],
        },
        "info_file": {
            "level": logging.INFO,
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": app_config.log_dir / "info.log",
            "mode": "a+",
            "backupCount": 3,
            "maxBytes": 5_000_000,
            "encoding": "utf-8",
            "filters": ["info_filter"],
        },
    },
    "formatters": {
        "default": {
            "format": "%(asctime)s [%(levelname)s] | %(name)s: %(funcName)s | %(message)s",
        },
    },
    "filters": {
        "error_filter": {
            "()": "src.config.log.ErrorFilter",
        },
        "info_filter": {
            "()": "src.config.log.InfoFilter",
        },
    },
}
