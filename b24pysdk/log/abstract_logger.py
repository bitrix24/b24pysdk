import logging
from typing import Any, ClassVar, Dict, Mapping, Optional, Text


class AbstractLogger:
    """"""

    NOTSET = logging.NOTSET
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    LOG_LEVELS: ClassVar[Dict[Text, int]] = {
        "NOTSET": NOTSET,
        "DEBUG": DEBUG,
        "INFO": INFO,
        "WARNING": WARNING,
        "ERROR": ERROR,
        "CRITICAL": CRITICAL,
    }

    @property
    def level(self) -> int:
        raise NotImplementedError

    def debug(self, message: Text, context: Optional[Mapping[Text, Any]] = None):
        raise NotImplementedError

    def info(self, message: Text, context: Optional[Mapping[Text, Any]] = None):
        raise NotImplementedError

    def warning(self, message: Text, context: Optional[Mapping[Text, Any]] = None):
        raise NotImplementedError

    def error(self, message: Text, context: Optional[Mapping[Text, Any]] = None):
        raise NotImplementedError

    def critical(self, message: Text, context: Optional[Mapping[Text, Any]] = None):
        raise NotImplementedError

    def log(self, level: int, message: Text, context: Optional[Mapping[Text, Any]] = None):
        raise NotImplementedError

    def set_level(self, level: int):
        raise NotImplementedError
