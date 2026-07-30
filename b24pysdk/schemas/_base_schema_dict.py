from abc import ABC
from typing import Dict, Generic, Text, Type

from ..utils.type_vars import BST, BSDataT, BSDictT

__all__ = [
    "BaseSchemaDict",
]


class BaseSchemaDict(dict[Text, BST], ABC, Generic[BST, BSDataT]):
    """
    Base dictionary for Bitrix24 schema values indexed by string keys.

    Subclasses should define ``_VALUE_SCHEMA`` with a schema class used to
    convert dictionary values from and to Bitrix24 format.
    """

    _VALUE_SCHEMA: Type[BST]

    @classmethod
    def from_bitrix(
            cls: Type[BSDictT],
            bitrix_data: Dict[Text, BSDataT],
            /,
    ) -> BSDictT:
        """
        Create a schema dictionary from Bitrix24 mapping data.

        Args:
            bitrix_data: Raw Bitrix24 mapping indexed by string keys.

        Returns:
            Schema dictionary with adapted values indexed by the same keys.
        """

        return cls({
            key: cls._VALUE_SCHEMA.from_bitrix(value_data)
            for key, value_data in bitrix_data.items()
        })

    def to_bitrix(self) -> Dict[Text, BSDataT]:
        """
        Convert the schema dictionary back to a Bitrix-compatible mapping.

        Returns:
            Dictionary indexed by Bitrix24 keys with raw Bitrix24 values.
        """
        return {
            key: value.to_bitrix()
            for key, value in self.items()
        }
