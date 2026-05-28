import logging

from .base_logger import BaseLogger


class NullLogger(BaseLogger):
    """
    Logger implementation that silently ignores all log records.

    Useful as a default logger when logging should be disabled without
    adding conditional checks around logging calls.
    """

    _DEFAULT_HANDLER_TYPE = logging.NullHandler
    _DEFAULT_LEVEL = logging.DEBUG
