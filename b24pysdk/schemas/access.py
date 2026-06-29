from dataclasses import dataclass
from typing import Dict, Text, TypedDict

from ..utils.dataclasses import frozen_dataclass_kwargs
from ._base_schema import BaseSchema
from ._base_schema_dict import BaseSchemaDict

__all__ = [
    "AccessName",
    "AccessNameData",
    "AccessNamesData",
    "AccessNamesDict",
]


class AccessNameData(TypedDict):
    provider: Text
    name: Text
    provider_id: Text


@dataclass(**frozen_dataclass_kwargs())
class AccessName(BaseSchema[AccessNameData]):
    """
    Single access permission description returned by the ``access.name`` method.
    """

    provider: Text
    name: Text
    provider_id: Text

    @classmethod
    def from_bitrix(cls, bitrix_data: AccessNameData, /) -> "AccessName":
        """
        Create an AccessNameItem schema from Bitrix24 access.name item data.

        Args:
            bitrix_data: Single access description from ``access.name`` result.

        Returns:
            AccessNameItem schema with Python-friendly fields.
        """
        return cls(
            provider=bitrix_data["provider"],
            name=bitrix_data["name"],
            provider_id=bitrix_data["provider_id"],
        )

    def to_bitrix(self) -> AccessNameData:
        """
        Convert the schema back to a Bitrix-compatible dictionary.

        Returns:
            Dictionary with Bitrix24 field names.
        """
        return {
            "provider": self.provider,
            "name": self.name,
            "provider_id": self.provider_id,
        }


AccessNamesData = Dict[Text, AccessNameData]


class AccessNamesDict(BaseSchemaDict[AccessName, AccessNameData]):
    """
    Result returned by the ``access.name`` method.

    The method returns access permission descriptions indexed by access
    identifier, for example ``G2`` or ``AU``.
    """
    _ITEM_SCHEMA = AccessName
