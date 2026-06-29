from dataclasses import dataclass
from typing import List, NoReturn, Optional, Text, TypedDict, Union

from ...utils.dataclasses import frozen_dataclass_kwargs
from .._base_listable_schema import BaseListableSchema
from .._base_schema import BaseSchema

__all__ = [
    "CRMStatusEntityItem",
    "CRMStatusEntityItemData",
    "CRMStatusEntityItemsData",
    "CRMStatusEntitySemanticInfo",
    "CRMStatusEntitySemanticInfoData",
    "CRMStatusEntityType",
    "CRMStatusEntityTypeData",
    "CRMStatusEntityTypesData",
]


class CRMStatusEntitySemanticInfoData(TypedDict):
    START_FIELD: Text
    FINAL_SUCCESS_FIELD: Text
    FINAL_UNSUCCESS_FIELD: Text
    FINAL_SORT: int


@dataclass(**frozen_dataclass_kwargs())
class CRMStatusEntitySemanticInfo(BaseSchema[CRMStatusEntitySemanticInfoData]):
    """
    Semantic status information for CRM status entity type.

    Returned inside ``SEMANTIC_INFO`` by ``crm.status.entity.types`` when the
    status entity supports semantic stages.
    """

    start_field: Text
    final_success_field: Text
    final_unsuccess_field: Text
    final_sort: int

    @classmethod
    def from_bitrix(cls, bitrix_data: CRMStatusEntitySemanticInfoData, /) -> "CRMStatusEntitySemanticInfo":
        """
        Create a CRMStatusEntitySemanticInfo schema from Bitrix24 data.

        Args:
            bitrix_data: Raw semantic information data.

        Returns:
            CRMStatusEntitySemanticInfo schema with Python-friendly field names.
        """
        return cls(
            start_field=bitrix_data["START_FIELD"],
            final_success_field=bitrix_data["FINAL_SUCCESS_FIELD"],
            final_unsuccess_field=bitrix_data["FINAL_UNSUCCESS_FIELD"],
            final_sort=bitrix_data["FINAL_SORT"],
        )

    def to_bitrix(self) -> CRMStatusEntitySemanticInfoData:
        """
        Convert the schema back to a Bitrix-compatible dictionary.

        Returns:
            Dictionary with Bitrix24 semantic information field names.
        """
        return {
            "START_FIELD": self.start_field,
            "FINAL_SUCCESS_FIELD": self.final_success_field,
            "FINAL_UNSUCCESS_FIELD": self.final_unsuccess_field,
            "FINAL_SORT": self.final_sort,
        }


class _CRMStatusEntityTypeOptionalData(TypedDict, total=False):
    ENTITY_TYPE_ID: int
    SEMANTIC_INFO: Union[CRMStatusEntitySemanticInfoData, List[NoReturn]]
    PREFIX: Text
    FIELD_ATTRIBUTE_SCOPE: Text
    IS_ENABLED: bool
    CATEGORY_ID: int
    PARENT_ID: Text
    CATEGORY_NAME: Text
    CATEGORY_SORT: int
    IS_DEFAULT_CATEGORY: bool


class CRMStatusEntityTypeData(_CRMStatusEntityTypeOptionalData):
    ID: Text
    NAME: Text


CRMStatusEntityTypesData = List[CRMStatusEntityTypeData]


@dataclass(**frozen_dataclass_kwargs())
class CRMStatusEntityType(BaseListableSchema[CRMStatusEntityTypeData]):
    """
    CRM status entity type returned by ``crm.status.entity.types``.

    The method returns supported CRM status dictionary identifiers such as
    lead statuses, sources, deal stages, and other CRM status entities.
    """

    bitrix_id: Text
    name: Text
    entity_type_id: Optional[int]
    semantic_info: Optional[CRMStatusEntitySemanticInfo]
    prefix: Optional[Text]
    field_attribute_scope: Optional[Text]
    is_enabled: Optional[bool]
    category_id: Optional[int]
    parent_id: Optional[Text]
    category_name: Optional[Text]
    category_sort: Optional[int]
    is_default_category: Optional[bool]

    @classmethod
    def from_bitrix(cls, bitrix_data: CRMStatusEntityTypeData, /) -> "CRMStatusEntityType":
        """
        Create a CRMStatusEntityType schema from Bitrix24 data.

        Args:
            bitrix_data: Raw CRM status entity type data.

        Returns:
            CRMStatusEntityType schema with Python-friendly field names.
        """
        return cls(
            bitrix_id=bitrix_data["ID"],
            name=bitrix_data["NAME"],
            entity_type_id=bitrix_data.get("ENTITY_TYPE_ID"),
            semantic_info=CRMStatusEntitySemanticInfo.from_bitrix(bitrix_data["SEMANTIC_INFO"]) if bitrix_data.get("SEMANTIC_INFO") else None,
            prefix=bitrix_data.get("PREFIX"),
            field_attribute_scope=bitrix_data.get("FIELD_ATTRIBUTE_SCOPE"),
            is_enabled=bitrix_data.get("IS_ENABLED"),
            category_id=int(bitrix_data["CATEGORY_ID"]) if "CATEGORY_ID" in bitrix_data else None,
            parent_id=bitrix_data.get("PARENT_ID"),
            category_name=bitrix_data.get("CATEGORY_NAME"),
            category_sort=bitrix_data.get("CATEGORY_SORT"),
            is_default_category=bitrix_data.get("IS_DEFAULT_CATEGORY"),
        )

    def to_bitrix(self) -> CRMStatusEntityTypeData:  # noqa: C901
        """
        Convert the schema back to a Bitrix-compatible dictionary.

        Returns:
            Dictionary with Bitrix24 CRM status entity type field names.
        """

        bitrix_data: CRMStatusEntityTypeData = {
            "ID": self.bitrix_id,
            "NAME": self.name,
        }

        if self.entity_type_id is not None:
            bitrix_data["ENTITY_TYPE_ID"] = self.entity_type_id

        if self.semantic_info is not None:
            bitrix_data["SEMANTIC_INFO"] = self.semantic_info.to_bitrix()
        else:
            bitrix_data["SEMANTIC_INFO"] = []

        if self.prefix is not None:
            bitrix_data["PREFIX"] = self.prefix

        if self.field_attribute_scope is not None:
            bitrix_data["FIELD_ATTRIBUTE_SCOPE"] = self.field_attribute_scope

        if self.is_enabled is not None:
            bitrix_data["IS_ENABLED"] = self.is_enabled

        if self.category_id is not None:
            bitrix_data["CATEGORY_ID"] = self.category_id

        if self.parent_id is not None:
            bitrix_data["PARENT_ID"] = self.parent_id

        if self.category_name is not None:
            bitrix_data["CATEGORY_NAME"] = self.category_name

        if self.category_sort is not None:
            bitrix_data["CATEGORY_SORT"] = self.category_sort

        if self.is_default_category is not None:
            bitrix_data["IS_DEFAULT_CATEGORY"] = self.is_default_category

        return bitrix_data


class CRMStatusEntityItemData(TypedDict):
    NAME: Text
    SORT: int
    STATUS_ID: Text


CRMStatusEntityItemsData = List[CRMStatusEntityItemData]


@dataclass(**frozen_dataclass_kwargs())
class CRMStatusEntityItem(BaseListableSchema[CRMStatusEntityItemData]):
    """
    CRM status entity item returned by ``crm.status.entity.items``.

    The method returns status dictionary items for the requested ``entityId``.
    """

    name: Text
    sort: int
    status_id: Text

    @classmethod
    def from_bitrix(cls, bitrix_data: CRMStatusEntityItemData, /) -> "CRMStatusEntityItem":
        """
        Create a CRMStatusEntityItem schema from Bitrix24 data.

        Args:
            bitrix_data: Raw CRM status entity item data.

        Returns:
            CRMStatusEntityItem schema with Python-friendly field names.
        """
        return cls(
            name=bitrix_data["NAME"],
            sort=bitrix_data["SORT"],
            status_id=bitrix_data["STATUS_ID"],
        )

    def to_bitrix(self) -> CRMStatusEntityItemData:
        """
        Convert the schema back to a Bitrix-compatible dictionary.

        Returns:
            Dictionary with Bitrix24 CRM status entity item field names.
        """
        return {
            "NAME": self.name,
            "SORT": self.sort,
            "STATUS_ID": self.status_id,
        }
