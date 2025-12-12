import typing

from ..utils import enum as _enum
from ..utils import types as _types

__all__ = [
    "DEFAULT_INITIAL_RETRY_DELAY",
    "DEFAULT_MAX_RETRIES",
    "DEFAULT_RETRY_DELAY_INCREMENT",
    "DEFAULT_TIMEOUT",
    "B24AppStatus",
    "B24BoolLit",
    "Protocol",
]


DEFAULT_INITIAL_RETRY_DELAY: typing.Final[_types.Number] = 1
""""""

DEFAULT_MAX_RETRIES: typing.Final[int] = 3
""""""

DEFAULT_RETRY_DELAY_INCREMENT: typing.Final[_types.Number] = 0
""""""

DEFAULT_TIMEOUT: typing.Final[_types.DefaultTimeout] = 10
""""""


class B24AppStatus(_enum.StrEnum):
    """"""

    FREE = "F"
    DEMO = "D"
    TRIAL = "T"
    PAID = "P"
    LOCAL = "L"
    SUBSCRIPTION = "S"

    @property
    def is_free(self) -> bool:
        return self == self.FREE

    @property
    def is_demo(self) -> bool:
        return self == self.DEMO

    @property
    def is_trial(self) -> bool:
        return self == self.TRIAL

    @property
    def is_paid(self) -> bool:
        return self == self.PAID

    @property
    def is_local(self) -> bool:
        return self == self.LOCAL

    @property
    def is_subscribtion(self) -> bool:
        return self == self.SUBSCRIPTION


class B24BoolLit(_enum.StrEnum):
    """"""

    TRUE = "Y"
    FALSE = "N"
    DEFAULT = "D"

    def __bool__(self):
        return bool(_types.B24Bool(self))


class Protocol(_enum.IntEnum):
    """"""
    HTTP = 0
    HTTPS = 1
