from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, Type

from ..utils.dataclasses import frozen_dataclass_kwargs
from ..utils.type_vars import BST, BSDataT

__all__ = [
    "BaseSchema",
]


@dataclass(**frozen_dataclass_kwargs())
class BaseSchema(ABC, Generic[BSDataT]):
    """
    Base class for structured Bitrix24 data without lifecycle.

    A schema:
    - does not store original Bitrix24 data;
    - converts Bitrix24 data to Python-friendly fields in ``from_bitrix()``;
    - may convert itself back to a Bitrix-compatible payload via ``to_bitrix()``;
    - must not implement lifecycle behavior such as save, update, delete, or refresh.
    """

    @classmethod
    @abstractmethod
    def from_bitrix(cls: Type[BST], bitrix_data: BSDataT, /) -> BST:
        """
        Create a schema instance from Bitrix24 data.

        Args:
            bitrix_data: Bitrix24 value or payload.

        Returns:
            Schema instance with converted Python fields.
        """
        raise NotImplementedError

    @abstractmethod
    def to_bitrix(self) -> BSDataT:
        """
        Convert the schema instance to a Bitrix-compatible value.

        Returns:
            Bitrix-compatible payload.
        """
        raise NotImplementedError
