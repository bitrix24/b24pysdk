from typing import TYPE_CHECKING, ClassVar, Generic, Optional, Text, TypeVar

from ....constants.list import ListIBlockType
from ..._fields import ObjectField
from ._base_list_element import BaseListElement, BaseListElementManager

if TYPE_CHECKING:
    from ....utils.types import Self
    from ..section.socnet_list_section import SocnetListSection  # noqa: F401

__all__ = [
    "SocnetListElement",
    "SocnetListElementManager",
]


class SocnetListElement(BaseListElement):
    """Element of a Bitrix24 social-network group list."""

    IBLOCK_TYPE_ID = ListIBlockType.LISTS_SOCNET
    SOCNET_GROUP_ID: ClassVar[Optional[int]] = None

    objects: "SocnetListElementManager[Self]"

    iblock_section = ObjectField["SocnetListSection"](
        BaseListElement.iblock_section_id,
        object_class="list.section",
        discriminator=(IBLOCK_TYPE_ID, None),
    )

    @property
    def url(self) -> Text:
        """Return the absolute Bitrix24 social-network list-element URL."""

        if self.IBLOCK_ID is None:
            raise ValueError("IBLOCK_ID is required to build the group-list element URL.")

        if self.SOCNET_GROUP_ID is None:
            raise ValueError("SOCNET_GROUP_ID is required to build the group-list element URL.")

        return (
            f"{self._base_url}/workgroups/group/{self.SOCNET_GROUP_ID}/"
            f"lists/{self.IBLOCK_ID}/element/0/{self.bitrix_pk}/"
        )


_SocnetListElementT = TypeVar("_SocnetListElementT", bound=SocnetListElement)


class SocnetListElementManager(BaseListElementManager[_SocnetListElementT], Generic[_SocnetListElementT]):
    """Manager for Bitrix24 social-network group list elements."""

    __slots__ = ()


SocnetListElement.objects = SocnetListElementManager()
