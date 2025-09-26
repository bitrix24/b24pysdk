import logging

from .base_logger import BaseLogger


class NullLogger(BaseLogger):
    """"""

    _DEFAULT_LEVEL = logging.DEBUG
    _DEFAULT_HANDLER_TYPE = logging.NullHandler
