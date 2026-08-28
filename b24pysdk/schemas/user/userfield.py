from dataclasses import dataclass
from typing import Annotated, Text, TypedDict, Union

from ...utils.converters import (
    bool_from_bitrix,
    bool_to_bitrix,
    int_from_bitrix,
    int_to_bitrix,
    text_from_bitrix,
    text_to_bitrix,
)
from ...utils.dataclasses import frozen_dataclass_kwargs
from ...utils.types import B24BoolStrictLiteral
from .._base_schema import BaseSchema

__all__ = [
    "UserUserfieldListItem",
    "UserUserfieldListItemData",
]


class UserUserfieldListItemData(TypedDict):
    """Raw Bitrix24 data for one list item of a user custom field."""
    ID: Union[int, Text]
    SORT: Union[int, Text]
    VALUE: Text
    DEF: Annotated[Text, B24BoolStrictLiteral]
    XML_ID: Text


@dataclass(**frozen_dataclass_kwargs())
class UserUserfieldListItem(BaseSchema[UserUserfieldListItemData]):
    """Single selectable value of a Bitrix24 user custom list field.

    ``sort`` has no default so its value must be specified explicitly when a
    schema instance is created locally.

    ``bitrix_id`` defaults to ``0`` because a new list item does not have an
    ID until Bitrix24 creates it. This keeps the public attribute typed as
    ``int`` instead of ``Optional[int]``.

    ``is_default`` defaults to ``False`` because a newly created list item is
    not the default option unless explicitly requested.

    ``xml_id`` defaults to an empty string because a caller does not need to
    provide an external identifier when creating a new list item.

    The raw ``UserUserfieldListItemData`` representation is always complete:
    ``ID``, ``SORT``, ``VALUE``, ``DEF`` and ``XML_ID`` are required keys.
    """

    value: Text
    sort: int
    bitrix_id: int = 0
    is_default: bool = False
    xml_id: Text = ""

    @classmethod
    def from_bitrix(cls, bitrix_data: UserUserfieldListItemData, /) -> "UserUserfieldListItem":
        """Create a list item schema from complete raw Bitrix24 list item data."""
        return cls(
            value=text_from_bitrix(bitrix_data["VALUE"], is_required=True),
            sort=int_from_bitrix(bitrix_data["SORT"], is_required=True),
            bitrix_id=int_from_bitrix(bitrix_data["ID"], is_required=True),
            is_default=bool_from_bitrix(bitrix_data["DEF"], is_required=True),
            xml_id=text_from_bitrix(bitrix_data["XML_ID"], is_required=True),
        )

    def to_bitrix(self) -> UserUserfieldListItemData:
        """Convert the schema to a complete Bitrix-compatible list item dictionary.

        All raw keys are always returned. For a newly created local schema,
        ``ID`` is ``0``, ``DEF`` is ``"N"`` and ``XML_ID`` is an empty string
        unless the caller explicitly supplies other values.
        """
        return {
            "ID": int_to_bitrix(self.bitrix_id, is_required=True),
            "SORT": int_to_bitrix(self.sort, is_required=True),
            "VALUE": text_to_bitrix(self.value, is_required=True),
            "DEF": bool_to_bitrix(self.is_default, is_required=True),
            "XML_ID": text_to_bitrix(self.xml_id, is_required=True),
        }
