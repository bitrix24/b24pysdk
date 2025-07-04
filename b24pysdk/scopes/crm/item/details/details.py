from ...base_crm import BaseCRM
from ..item import Item
from .configuration import Configuration


class Details(BaseCRM):
    """"""

    __slots__ = ("_item",)

    def __init__(self, item: Item):
        super().__init__(item._scope)
        self._item = item
        self._path = self._get_path(item)

    @property
    def configuration(self) -> Configuration:
        """"""
        return Configuration(self)

    @property
    def entity_type_id(self) -> int:
        """"""
        return self._item.ENTITY_TYPE_ID
