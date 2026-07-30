from abc import ABC
from dataclasses import dataclass
from typing import Generic, List, Optional, Text, TypedDict

from ...utils.converters import int_from_bitrix, int_to_bitrix, text_from_bitrix, text_to_bitrix
from ...utils.dataclasses import frozen_dataclass_kwargs
from ...utils.type_vars import BSDataT
from .._base_schema import BaseSchema

__all__ = [
    "CRMEnumItem",
    "CRMEnumItemData",
    "CRMEnumItemsData",
    "OrderOwnerType",
    "OrderOwnerTypeData",
    "OrderOwnerTypesData",
]


@dataclass(**frozen_dataclass_kwargs())
class _BaseCRMEnumItem(BaseSchema[BSDataT], ABC, Generic[BSDataT]):
    """
    Base class for CRM enum-like items.

    It stores common Python-friendly fields shared by CRM enum schemas.
    """
    bitrix_id: int
    name: Text


class CRMEnumItemData(TypedDict):
    ID: int
    NAME: Text
    SYMBOL_CODE: Optional[Text]
    SYMBOL_CODE_SHORT: Optional[Text]


CRMEnumItemsData = List[CRMEnumItemData]


@dataclass(**frozen_dataclass_kwargs())
class CRMEnumItem(_BaseCRMEnumItem[CRMEnumItemData]):
    """
    Single CRM enum item returned by most ``crm.enum.*`` methods.

    Suitable for methods returning enum items with the common Bitrix24 shape:

        {
            "ID": 1,
            "NAME": "...",
            "SYMBOL_CODE": "...",
            "SYMBOL_CODE_SHORT": "...",
        }
    """

    symbol_code: Optional[Text]
    symbol_code_short: Optional[Text]

    @classmethod
    def from_bitrix(cls, bitrix_data: CRMEnumItemData, /) -> "CRMEnumItem":
        """
        Create a CRMEnumItem schema from Bitrix24 enum item data.

        Args:
            bitrix_data: Raw CRM enum item data.

        Returns:
            CRMEnumItem schema with Python-friendly field names.
        """
        return cls(
            bitrix_id=int_from_bitrix(bitrix_data["ID"], is_required=True),
            name=text_from_bitrix(bitrix_data["NAME"], is_required=True),
            symbol_code=text_from_bitrix(bitrix_data["SYMBOL_CODE"]),
            symbol_code_short=text_from_bitrix(bitrix_data["SYMBOL_CODE_SHORT"]),
        )

    def to_bitrix(self) -> CRMEnumItemData:
        """
        Convert the schema back to a Bitrix-compatible dictionary.

        Returns:
            Dictionary with Bitrix24 CRM enum item field names.
        """
        return {
            "ID": int_to_bitrix(self.bitrix_id, is_required=True),
            "NAME": text_to_bitrix(self.name, is_required=True),
            "SYMBOL_CODE": text_to_bitrix(self.symbol_code),
            "SYMBOL_CODE_SHORT": text_to_bitrix(self.symbol_code_short),
        }


class OrderOwnerTypeData(TypedDict):
    attribute: Text
    code: Text
    id: int
    name: Text


OrderOwnerTypesData = List[OrderOwnerTypeData]


@dataclass(**frozen_dataclass_kwargs())
class OrderOwnerType(_BaseCRMEnumItem[OrderOwnerTypeData]):
    """
    Single order owner type returned by ``crm.enum.getorderownertypes``.

    This method uses a different response shape from common ``crm.enum.*``
    methods, so it has a separate schema.
    """

    attribute: Text
    code: Text

    @classmethod
    def from_bitrix(cls, bitrix_data: OrderOwnerTypeData, /) -> "OrderOwnerType":
        """
        Create an OrderOwnerType schema from Bitrix24 order owner type data.

        Args:
            bitrix_data: Raw order owner type data.

        Returns:
            OrderOwnerType schema with Python-friendly field names.
        """
        return cls(
            bitrix_id=int_from_bitrix(bitrix_data["id"], is_required=True),
            name=text_from_bitrix(bitrix_data["name"], is_required=True),
            attribute=text_from_bitrix(bitrix_data["attribute"], is_required=True),
            code=text_from_bitrix(bitrix_data["code"], is_required=True),
        )

    def to_bitrix(self) -> OrderOwnerTypeData:
        """
        Convert the schema back to a Bitrix-compatible dictionary.

        Returns:
            Dictionary with Bitrix24 order owner type field names.
        """
        return {
            "attribute": text_to_bitrix(self.attribute, is_required=True),
            "code": text_to_bitrix(self.code, is_required=True),
            "id": int_to_bitrix(self.bitrix_id, is_required=True),
            "name": text_to_bitrix(self.name, is_required=True),
        }
