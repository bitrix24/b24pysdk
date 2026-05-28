import logging
from typing import Any, ClassVar, Dict, Mapping, Optional, Text


class AbstractLogger:
    """
    Base logger interface used by the SDK.

    Defines common logging levels and the logging methods expected from
    concrete logger implementations.
    """

    NOTSET: int = logging.NOTSET
    DEBUG: int = logging.DEBUG
    INFO: int = logging.INFO
    WARNING: int = logging.WARNING
    ERROR: int = logging.ERROR
    CRITICAL: int = logging.CRITICAL

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
