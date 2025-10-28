from functools import cached_property

from .._base_crm import BaseCRM
from .trigger import Trigger

__all__ = [
    "Automation",
]


class Automation(BaseCRM):
    """"""

    @cached_property
    def trigger(self) -> Trigger:
        """"""
        return Trigger(self)
