from dataclasses import dataclass
from typing import Annotated, Dict, List, Optional, Text, TypedDict

from ...constants.userfield import UserTypeID
from ...utils.converters import bool_from_bitrix, text_from_bitrix, text_to_bitrix
from ...utils.dataclasses import frozen_dataclass_kwargs
from ...utils.types import UserTypeIDLiteral
from .._base_schema import BaseSchema
from .._base_schema_dict import BaseSchemaDict

__all__ = [
    "CRMUserfieldField",
    "CRMUserfieldFieldData",
    "CRMUserfieldFieldsData",
    "CRMUserfieldFieldsDict",
    "CRMUserfieldType",
    "CRMUserfieldTypeData",
    "CRMUserfieldTypesData",
]


class _CRMUserfieldFieldOptionalData(TypedDict, total=False):
    isReadOnly: bool
    isImmutable: bool
    isMultiple: bool


class CRMUserfieldFieldData(_CRMUserfieldFieldOptionalData):
    type: Text
    title: Text


CRMUserfieldFieldsData = Dict[Text, CRMUserfieldFieldData]


@dataclass(**frozen_dataclass_kwargs())
class CRMUserfieldField(BaseSchema[CRMUserfieldFieldData]):
    """Field description returned by CRM user field metadata methods."""

    type: Text
    title: Text
    is_read_only: Optional[bool] = None
    is_immutable: Optional[bool] = None
    is_multiple: Optional[bool] = None

    @classmethod
    def from_bitrix(cls, bitrix_data: CRMUserfieldFieldData, /) -> "CRMUserfieldField":
        """Create a user field description schema from Bitrix24 data."""
        return cls(
            type=text_from_bitrix(bitrix_data["type"], is_required=True),
            title=text_from_bitrix(bitrix_data["title"], is_required=True),
            is_read_only=bool_from_bitrix(bitrix_data.get("isReadOnly")),
            is_immutable=bool_from_bitrix(bitrix_data.get("isImmutable")),
            is_multiple=bool_from_bitrix(bitrix_data.get("isMultiple")),
        )

    def to_bitrix(self) -> CRMUserfieldFieldData:
        """Convert the schema back to a Bitrix-compatible dictionary."""

        bitrix_data: CRMUserfieldFieldData = {
            "type": text_to_bitrix(self.type, is_required=True),
            "title": text_to_bitrix(self.title, is_required=True),
        }

        if self.is_read_only is not None:
            bitrix_data["isReadOnly"] = bool_from_bitrix(self.is_read_only, is_required=True)

        if self.is_immutable is not None:
            bitrix_data["isImmutable"] = bool_from_bitrix(self.is_immutable, is_required=True)

        if self.is_multiple is not None:
            bitrix_data["isMultiple"] = bool_from_bitrix(self.is_multiple, is_required=True)

        return bitrix_data


class CRMUserfieldFieldsDict(BaseSchemaDict[CRMUserfieldField, CRMUserfieldFieldData]):
    """Field descriptions returned by CRM user field metadata methods."""
    _VALUE_SCHEMA = CRMUserfieldField


class CRMUserfieldTypeData(TypedDict):
    ID: Annotated[Text, UserTypeIDLiteral]
    title: Text


CRMUserfieldTypesData = List[CRMUserfieldTypeData]


@dataclass(**frozen_dataclass_kwargs())
class CRMUserfieldType(BaseSchema[CRMUserfieldTypeData]):
    """User field type returned by ``crm.userfield.types``."""

    bitrix_id: UserTypeID
    title: Text

    @classmethod
    def from_bitrix(cls, bitrix_data: CRMUserfieldTypeData, /) -> "CRMUserfieldType":
        """Create a user field type schema from Bitrix24 data."""
        return cls(
            bitrix_id=UserTypeID(bitrix_data["ID"]),
            title=text_from_bitrix(bitrix_data["title"], is_required=True),
        )

    def to_bitrix(self) -> CRMUserfieldTypeData:
        """Convert the schema back to a Bitrix-compatible dictionary."""
        return {
            "ID": self.bitrix_id.value,
            "title": text_to_bitrix(self.title, is_required=True),
        }
