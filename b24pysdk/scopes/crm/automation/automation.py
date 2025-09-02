from ..base_crm import BaseCRM
from .trigger import Trigger


class Automation(BaseCRM):
    """"""

    @property
    def trigger(self) -> Trigger:
        """"""
        return Trigger(self)
