from dataclasses import dataclass
from typing import List, NoReturn, Optional, Text, TypedDict, Union

from ...utils.converters import bool_from_bitrix, int_from_bitrix, int_to_bitrix, text_from_bitrix, text_to_bitrix
from ...utils.dataclasses import frozen_dataclass_kwargs
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
            start_field=text_from_bitrix(bitrix_data["START_FIELD"], is_required=True),
            final_success_field=text_from_bitrix(bitrix_data["FINAL_SUCCESS_FIELD"], is_required=True),
            final_unsuccess_field=text_from_bitrix(bitrix_data["FINAL_UNSUCCESS_FIELD"], is_required=True),
            final_sort=int_from_bitrix(bitrix_data["FINAL_SORT"], is_required=True),
        )

    def to_bitrix(self) -> CRMStatusEntitySemanticInfoData:
        """
        Convert the schema back to a Bitrix-compatible dictionary.

        Returns:
            Dictionary with Bitrix24 semantic information field names.
        """
        return {
            "START_FIELD": text_to_bitrix(self.start_field, is_required=True),
            "FINAL_SUCCESS_FIELD": text_to_bitrix(self.final_success_field, is_required=True),
            "FINAL_UNSUCCESS_FIELD": text_to_bitrix(self.final_unsuccess_field, is_required=True),
            "FINAL_SORT": int_to_bitrix(self.final_sort, is_required=True),
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
class CRMStatusEntityType(BaseSchema[CRMStatusEntityTypeData]):
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
            bitrix_id=text_from_bitrix(bitrix_data["ID"], is_required=True),
            name=text_from_bitrix(bitrix_data["NAME"], is_required=True),
            entity_type_id=int_from_bitrix(bitrix_data.get("ENTITY_TYPE_ID")),
            semantic_info=CRMStatusEntitySemanticInfo.from_bitrix(bitrix_data["SEMANTIC_INFO"]) if bitrix_data.get("SEMANTIC_INFO") else None,
            prefix=text_from_bitrix(bitrix_data.get("PREFIX")),
            field_attribute_scope=text_from_bitrix(bitrix_data.get("FIELD_ATTRIBUTE_SCOPE")),
            is_enabled=bool_from_bitrix(bitrix_data.get("IS_ENABLED")),
            category_id=int_from_bitrix(bitrix_data.get("CATEGORY_ID")),
            parent_id=text_from_bitrix(bitrix_data.get("PARENT_ID")),
            category_name=text_from_bitrix(bitrix_data.get("CATEGORY_NAME")),
            category_sort=int_from_bitrix(bitrix_data.get("CATEGORY_SORT")),
            is_default_category=bool_from_bitrix(bitrix_data.get("IS_DEFAULT_CATEGORY")),
        )

    def to_bitrix(self) -> CRMStatusEntityTypeData:  # noqa: C901
        """
        Convert the schema back to a Bitrix-compatible dictionary.

        Returns:
            Dictionary with Bitrix24 CRM status entity type field names.
        """

        bitrix_data: CRMStatusEntityTypeData = {
            "ID": text_to_bitrix(self.bitrix_id, is_required=True),
            "NAME": text_to_bitrix(self.name, is_required=True),
        }

        if self.entity_type_id is not None:
            bitrix_data["ENTITY_TYPE_ID"] = int_to_bitrix(self.entity_type_id, is_required=True)

        if self.semantic_info is not None:
            bitrix_data["SEMANTIC_INFO"] = self.semantic_info.to_bitrix()
        else:
            bitrix_data["SEMANTIC_INFO"] = []

        if self.prefix is not None:
            bitrix_data["PREFIX"] = text_to_bitrix(self.prefix, is_required=True)

        if self.field_attribute_scope is not None:
            bitrix_data["FIELD_ATTRIBUTE_SCOPE"] = text_to_bitrix(self.field_attribute_scope, is_required=True)

        if self.is_enabled is not None:
            bitrix_data["IS_ENABLED"] = bool_from_bitrix(self.is_enabled, is_required=True)

        if self.category_id is not None:
            bitrix_data["CATEGORY_ID"] = int_to_bitrix(self.category_id, is_required=True)

        if self.parent_id is not None:
            bitrix_data["PARENT_ID"] = text_to_bitrix(self.parent_id, is_required=True)

        if self.category_name is not None:
            bitrix_data["CATEGORY_NAME"] = text_to_bitrix(self.category_name, is_required=True)

        if self.category_sort is not None:
            bitrix_data["CATEGORY_SORT"] = int_to_bitrix(self.category_sort, is_required=True)

        if self.is_default_category is not None:
            bitrix_data["IS_DEFAULT_CATEGORY"] = bool_from_bitrix(self.is_default_category, is_required=True)

        return bitrix_data


class CRMStatusEntityItemData(TypedDict):
    NAME: Text
    SORT: int
    STATUS_ID: Text


CRMStatusEntityItemsData = List[CRMStatusEntityItemData]


@dataclass(**frozen_dataclass_kwargs())
class CRMStatusEntityItem(BaseSchema[CRMStatusEntityItemData]):
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
            name=text_from_bitrix(bitrix_data["NAME"], is_required=True),
            sort=int_from_bitrix(bitrix_data["SORT"], is_required=True),
            status_id=text_from_bitrix(bitrix_data["STATUS_ID"], is_required=True),
        )

    def to_bitrix(self) -> CRMStatusEntityItemData:
        """
        Convert the schema back to a Bitrix-compatible dictionary.

        Returns:
            Dictionary with Bitrix24 CRM status entity item field names.
        """
        return {
            "NAME": text_to_bitrix(self.name, is_required=True),
            "SORT": int_to_bitrix(self.sort, is_required=True),
            "STATUS_ID": text_to_bitrix(self.status_id, is_required=True),
        }
