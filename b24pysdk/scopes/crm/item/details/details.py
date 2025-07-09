from ...base_crm import BaseCRM
from ..item import Item
from .configuration import Configuration


class Details(BaseCRM):
    """"""

    def __init__(self, item: Item):
        super().__init__(item._scope)
        self._path = self._get_path(item)

    @property
    def configuration(self) -> Configuration:
        """"""
        return Configuration(self)
