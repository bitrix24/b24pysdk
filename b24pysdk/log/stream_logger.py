import logging
from typing import Iterable, Optional, Text

from .base_logger import BaseLogger


class StreamLogger(BaseLogger):
    """"""

    _DEFAULT_LEVEL = logging.DEBUG
    _DEFAULT_HANDLER_TYPE = logging.StreamHandler
    _FMT: Text = "%(asctime)s [%(levelname)s] %(message)s"

    _formatter: Optional[logging.Formatter]

    class ContextFormatter(logging.Formatter):

        def format(self, record: logging.LogRecord) -> Text:
            message = super().format(record)
            context = getattr(record, "context", None)

            if context:
                message = f"{message} | context: {context}"

            return message

    def __init__(
            self,
            *,
            name: Optional[Text] = None,
            handlers: Optional[Iterable[logging.Handler]] = None,
            formatter: Optional[logging.Formatter] = None,
    ):
        self._formatter = formatter or self.ContextFormatter(self.get_fmt())
        super().__init__(name=name, handlers=handlers)

    @classmethod
    def get_fmt(cls) -> Text:
        return cls._FMT

    @property
    def formatter(self) -> logging.Formatter:
        return self._formatter

    def set_handler(self, handler: logging.Handler):
        handler.setFormatter(self._formatter)
        super().set_handler(handler)

    def set_formatter(self, formatter: logging.Formatter):
        self._formatter = formatter

        for handler in self._logger.handlers:
            handler.setFormatter(self._formatter)
