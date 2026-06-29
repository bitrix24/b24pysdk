from abc import ABC
from dataclasses import dataclass
from typing import Generic, List, Optional, Text, TypedDict

from ...utils.dataclasses import frozen_dataclass_kwargs
from ...utils.type_vars import BSDataT
from .._base_listable_schema import BaseListableSchema

__all__ = [
    "CRMEnumItem",
    "CRMEnumItemBase",
    "CRMEnumItemData",
    "CRMEnumItemsData",
    "OrderOwnerType",
    "OrderOwnerTypeData",
    "OrderOwnerTypesData",
]


@dataclass(**frozen_dataclass_kwargs())
class CRMEnumItemBase(BaseListableSchema[BSDataT], ABC, Generic[BSDataT]):
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
class CRMEnumItem(CRMEnumItemBase[CRMEnumItemData]):
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
            bitrix_id=int(bitrix_data["ID"]),
            name=bitrix_data["NAME"],
            symbol_code=bitrix_data["SYMBOL_CODE"],
            symbol_code_short=bitrix_data["SYMBOL_CODE_SHORT"],
        )

    def to_bitrix(self) -> CRMEnumItemData:
        """
        Convert the schema back to a Bitrix-compatible dictionary.

        Returns:
            Dictionary with Bitrix24 CRM enum item field names.
        """
        return {
            "ID": self.bitrix_id,
            "NAME": self.name,
            "SYMBOL_CODE": self.symbol_code,
            "SYMBOL_CODE_SHORT": self.symbol_code_short,
        }


class OrderOwnerTypeData(TypedDict):
    attribute: Text
    code: Text
    id: int
    name: Text


OrderOwnerTypesData = List[OrderOwnerTypeData]


@dataclass(**frozen_dataclass_kwargs())
class OrderOwnerType(CRMEnumItemBase[OrderOwnerTypeData]):
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
            bitrix_id=int(bitrix_data["id"]),
            name=bitrix_data["name"],
            attribute=bitrix_data["attribute"],
            code=bitrix_data["code"],
        )

    def to_bitrix(self) -> OrderOwnerTypeData:
        """
        Convert the schema back to a Bitrix-compatible dictionary.

        Returns:
            Dictionary with Bitrix24 order owner type field names.
        """
        return {
            "attribute": self.attribute,
            "code": self.code,
            "id": self.bitrix_id,
            "name": self.name,
        }
