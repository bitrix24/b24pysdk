import logging
from typing import Any, Iterable, List, Mapping, Optional, Text, Type

from ..version import SDK_NAME
from .abstract_logger import AbstractLogger


class BaseLogger(AbstractLogger):
    """"""

    _DEFAULT_HANDLER_TYPE: Type[logging.Handler]
    _DEFAULT_LEVEL: int

    __slots__ = ("_logger", "_name")

    _logger: logging.Logger
    _name: Text

    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(*args, **kwargs)

        required_attrs = {
            "_DEFAULT_LEVEL": "int",
            "_DEFAULT_HANDLER_TYPE": "Type[logging.Handler]",
        }

        for attr, hint in required_attrs.items():
            if attr not in cls.__dict__:
                raise TypeError(
                    f"{cls.__name__!r} must define class attribute {attr!r} ({hint})",
                )

    def __init__(
            self,
            *,
            name: Optional[Text] = None,
            level: Optional[int] = None,
            handlers: Optional[Iterable[logging.Handler]] = None,
    ):
        self._name = name or self.get_default_logger_name()

        self._logger = logging.getLogger(self._name)
        self._logger.propagate = False

        self.set_level(level or self.get_default_level())

        if not self.handlers:
            for handler in (handlers or (self.get_default_handler_type()(),)):
                self.set_handler(handler)

    @classmethod
    def get_default_logger_name(cls) -> Text:
        return f"{SDK_NAME}_{cls.__name__}"

    @classmethod
    def get_default_level(cls) -> int:
        return cls._DEFAULT_LEVEL

    @classmethod
    def get_default_handler_type(cls) -> Type[logging.Handler]:
        return cls._DEFAULT_HANDLER_TYPE

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    @property
    def handlers(self) -> List[logging.Handler]:
        return self._logger.handlers

    @property
    def level(self) -> int:
        return self._logger.level

    def _log(
            self,
            level: int,
            message: Text,
            context: Optional[Mapping[Text, Any]] = None,
    ):
        self._logger.log(level, message, extra={"context": context or {}})

    def debug(
            self,
            message: Text,
            context: Optional[Mapping[Text, Any]] = None,
    ):
        self._log(self.DEBUG, message, context)

    def info(
            self,
            message: Text,
            context: Optional[Mapping[Text, Any]] = None,
    ):
        self._log(self.INFO, message, context)

    def warning(
            self,
            message: Text,
            context: Optional[Mapping[Text, Any]] = None,
    ):
        self._log(self.WARNING, message, context)

    def error(
            self,
            message: Text,
            context: Optional[Mapping[Text, Any]] = None,
    ):
        self._log(self.ERROR, message, context)

    def critical(
            self,
            message: Text,
            context: Optional[Mapping[Text, Any]] = None,
    ):
        self._log(self.CRITICAL, message, context)

    def log(
            self,
            level: int,
            message: Text,
            context: Optional[Mapping[Text, Any]] = None,
    ):
        self._log(level, message, context)

    def set_level(self, level: int):
        self._logger.setLevel(level)

        for handler in self.handlers:
            handler.setLevel(level)

    def set_handler(self, handler: logging.Handler):
        handler.setLevel(self.level)
        self._logger.addHandler(handler)

    def remove_handler(self, handler: logging.Handler):
        self._logger.removeHandler(handler)

    def clear_handlers(self):
        self._logger.handlers.clear()
