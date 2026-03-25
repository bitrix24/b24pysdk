from functools import cached_property

from ..._base_entity import BaseEntity
from .report import Report
from .reports import Reports
from .settings import Settings

__all__ = [
    "Timecontrol",
]


class Timecontrol(BaseEntity):
    """"""

    @cached_property
    def report(self) -> Report:
        """"""
        return Report(self)

    @cached_property
    def reports(self) -> Reports:
        """"""
        return Reports(self)

    @cached_property
    def settings(self) -> Settings:
        """"""
        return Settings(self)
