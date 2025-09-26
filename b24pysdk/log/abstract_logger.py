import logging
from abc import ABC, abstractmethod
from typing import Any, ClassVar, Dict, Mapping, Optional, Text


class AbstractLogger(ABC):
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
    @abstractmethod
    def level(self) -> int: ...

    @abstractmethod
    def debug(self, message: Text, context: Optional[Mapping[Text, Any]] = None): ...

    @abstractmethod
    def info(self, message: Text, context: Optional[Mapping[Text, Any]] = None): ...

    @abstractmethod
    def warning(self, message: Text, context: Optional[Mapping[Text, Any]] = None): ...

    @abstractmethod
    def error(self, message: Text, context: Optional[Mapping[Text, Any]] = None): ...

    @abstractmethod
    def critical(self, message: Text, context: Optional[Mapping[Text, Any]] = None): ...

    @abstractmethod
    def log(self, level: int, message: Text, context: Optional[Mapping[Text, Any]] = None): ...

    @abstractmethod
    def set_level(self, level: int): ...
