from abc import ABC
from dataclasses import dataclass
from typing import ClassVar, Generator, Generic, List, Optional, Text, Type, Union, overload

from ..utils.dataclasses import frozen_dataclass_kwargs
from ..utils.type_vars import BSLT, BSDataT
from ..utils.types import JSONDict
from ._base_schema import BaseSchema

__all__ = [
    "BaseListableSchema",
]


@dataclass(**frozen_dataclass_kwargs())
class BaseListableSchema(BaseSchema[BSDataT], ABC, Generic[BSDataT]):
    """
    Base class for Bitrix24 schemas that can also adapt list-like results.

    A listable schema represents a single Bitrix24 item through
    ``from_bitrix()`` and can additionally adapt method results through
    ``from_bitrix_result()``:

    - wrapped result object, for example ``{"items": [...]}``;
    - raw list returned by regular list loading;
    - raw generator returned by fast list loading.
    """

    _WRAPPER: ClassVar[Optional[Text]] = None

    @classmethod
    @overload
    def from_bitrix_result(cls: Type[BSLT], bitrix_result: List[BSDataT], /) -> List[BSLT]: ...

    @classmethod
    @overload
    def from_bitrix_result(cls: Type[BSLT], bitrix_result: Generator[BSDataT, None, None], /) -> Generator[BSLT, None, None]: ...

    @classmethod
    @overload
    def from_bitrix_result(cls: Type[BSLT], bitrix_result: JSONDict, /) -> List[BSLT]: ...

    @classmethod
    def from_bitrix_result(
            cls: Type[BSLT],
            bitrix_result: Union[List[BSDataT], Generator[BSDataT, None, None], JSONDict],
            /,
    ) -> Union[List[BSLT], Generator[BSLT, None, None]]:
        """
        Adapt a Bitrix24 method result to Python-friendly schema values.

        Args:
            bitrix_result: Raw Bitrix24 ``result`` value. It can be a wrapped
                object, a list, or a generator.

        Returns:
            List of schema instances for materialized results, or a generator
            of schema instances for fast list results.
        """

        if isinstance(bitrix_result, list):
            return [cls.from_bitrix(bitrix_data) for bitrix_data in bitrix_result]

        if isinstance(bitrix_result, dict):
            return [cls.from_bitrix(bitrix_data) for bitrix_data in cls._unwrap_bitrix_result(bitrix_result)]

        return (cls.from_bitrix(bitrix_data) for bitrix_data in bitrix_result)

    @classmethod
    def _unwrap_bitrix_result(cls, bitrix_result: JSONDict, /) -> List[BSDataT]:
        """
        Extract wrapped list-like Bitrix24 result.

        Args:
            bitrix_result: Raw wrapped Bitrix24 ``result`` object.

        Returns:
            Raw item list stored under ``_WRAPPER``.

        Raises:
            TypeError: If ``_WRAPPER`` is not configured or wrapped value is
                not a list.
        """

        if cls._WRAPPER is None:
            raise TypeError(f"{cls.__name__!r} cannot adapt wrapped Bitrix24 result without _WRAPPER.")

        if cls._WRAPPER not in bitrix_result:
            raise TypeError(
                f"{cls.__name__!r} expected wrapped Bitrix24 result "
                f"to contain {cls._WRAPPER!r} key.",
            )

        unwrapped_bitrix_result = bitrix_result[cls._WRAPPER]

        if not isinstance(unwrapped_bitrix_result, list):
            raise TypeError(
                f"{cls.__name__!r} expected Bitrix24 result under key {cls._WRAPPER!r} "
                f"to be a list, got {type(unwrapped_bitrix_result).__name__}.",
            )

        return unwrapped_bitrix_result
