from functools import cached_property

from .._base_crm import BaseCRM
from .mode import Mode

__all__ = [
    "Settings",
]


class Settings(BaseCRM):
    """"""

    @cached_property
    def mode(self) -> Mode:
        """"""
        return Mode(self)
