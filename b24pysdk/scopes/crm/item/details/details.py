from typing import TYPE_CHECKING

from ...base_crm import BaseCRM
from .configuration import Configuration

if TYPE_CHECKING:
    from ..base_item import BaseItem


class Details(BaseCRM):
    """"""

    def __init__(self, item: "BaseItem"):
        super().__init__(item._scope)
        self._path = self._get_path(item)

    @property
    def configuration(self) -> Configuration:
        """"""
        return Configuration(self)
