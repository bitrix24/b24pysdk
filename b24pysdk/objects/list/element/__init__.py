from typing import TYPE_CHECKING, Generic, Text, TypeVar

from ....constants.list import ListIBlockType
from ..._fields import ObjectField
from ._base_list_element import BaseListElement, BaseListElementManager

if TYPE_CHECKING:
    from ....utils.types import Self
    from ..section import ListSection  # noqa: F401

__all__ = [
    "ListElement",
    "ListElementManager",
]


class ListElement(BaseListElement):
    """Element of a Bitrix24 universal list."""

    IBLOCK_TYPE_ID = ListIBlockType.LISTS

    objects: "ListElementManager[Self]"

    iblock_section = ObjectField["ListSection"](
        BaseListElement.iblock_section_id,
        object_class="list.section",
        discriminator=(IBLOCK_TYPE_ID, None),
    )

    @property
    def url(self) -> Text:
        """Return the absolute Bitrix24 universal-list element URL."""

        if self.IBLOCK_ID is None:
            raise ValueError("IBLOCK_ID is required to build the list-element URL.")

        return f"{self._base_url}/company/lists/{self.IBLOCK_ID}/element/0/{self.bitrix_pk}/"


_ListElementT = TypeVar("_ListElementT", bound=ListElement)


class ListElementManager(BaseListElementManager[_ListElementT], Generic[_ListElementT]):
    """Manager for Bitrix24 universal-list elements."""

    __slots__ = ()


ListElement.objects = ListElementManager()
