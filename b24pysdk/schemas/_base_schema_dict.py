from abc import ABC
from typing import Dict, Generic, Optional, Text, Type, Union

from ..utils.type_vars import BSDT, BST, BSDataT

__all__ = [
    "BaseSchemaDict",
]


class BaseSchemaDict(dict[Text, BST], ABC, Generic[BST, BSDataT]):
    """
    Base dictionary for Bitrix24 schema values indexed by string keys.

    Subclasses should define ``_ITEM_SCHEMA`` with a schema class used to
    convert dictionary values from and to Bitrix24 format.
    """

    _ITEM_SCHEMA: Type[BST]
    _WRAPPER: Optional[Text] = None

    @classmethod
    def from_bitrix(
            cls: Type[BSDT],
            bitrix_data: Union[Dict[Text, BSDataT], Dict[Text, Dict[Text, BSDataT]]],
            /,
    ) -> BSDT:
        """
        Create a schema dictionary from Bitrix24 mapping data.

        Args:
            bitrix_data: Raw Bitrix24 mapping indexed by string keys. If
                ``_WRAPPER`` is configured, the mapping is first extracted from
                that root key.

        Returns:
            Schema dictionary with adapted values indexed by the same keys.
        """

        bitrix_data = cls._unwrap_bitrix_data(bitrix_data)

        return cls({
            key: cls._ITEM_SCHEMA.from_bitrix(item_data)
            for key, item_data in bitrix_data.items()
        })

    @classmethod
    def _unwrap_bitrix_data(cls, bitrix_data: Union[Dict[Text, BSDataT], Dict[Text, Dict[Text, BSDataT]]], /) -> Dict[Text, BSDataT]:
        """
        Extract wrapped dictionary-like Bitrix24 data when ``_WRAPPER`` is set.

        Args:
            bitrix_data: Raw Bitrix24 data passed to the schema adapter.

        Returns:
            Raw mapping to be adapted into schema values.
        """

        if cls._WRAPPER is None or next(iter(bitrix_data.keys())) != cls._WRAPPER:
            return bitrix_data

        unwrapped_bitrix_data = bitrix_data[cls._WRAPPER]

        if not isinstance(unwrapped_bitrix_data, dict):
            raise TypeError(
                f"{cls.__name__!r} expected Bitrix24 data under key {cls._WRAPPER!r} "
                f"to be a dict, got {type(unwrapped_bitrix_data).__name__}.",
            )

        return unwrapped_bitrix_data

    def to_bitrix(self) -> Dict[Text, BSDataT]:
        """
        Convert the schema dictionary back to a Bitrix-compatible mapping.

        Returns:
            Dictionary indexed by Bitrix24 keys with raw Bitrix24 values.
        """
        return {
            key: item.to_bitrix()
            for key, item in self.items()
        }
