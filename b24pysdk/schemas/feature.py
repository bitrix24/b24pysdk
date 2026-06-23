from dataclasses import dataclass
from typing import Annotated, Optional, Text, TypedDict

from ..utils.converters import bool_from_bitrix, bool_to_bitrix
from ..utils.dataclasses import frozen_dataclass_kwargs
from ..utils.types import B24BoolStrictLiteral
from ._base_schema import BaseSchema

__all__ = [
    "FeatureGet",
    "FeatureGetData",
]


class _FeatureGetOptionalData(TypedDict, total=False):
    lang_selfhosted: Text


class FeatureGetData(_FeatureGetOptionalData):
    value: Annotated[Text, B24BoolStrictLiteral]


@dataclass(**frozen_dataclass_kwargs())
class FeatureGet(BaseSchema[FeatureGetData]):
    """
    Result returned by the ``feature.get`` method.

    The method returns whether a specific Bitrix24 feature is available on
    the current portal.
    """

    value: bool
    lang_selfhosted: Optional[Text]

    @classmethod
    def from_bitrix(cls, bitrix_data: FeatureGetData, /) -> "FeatureGet":
        """
        Create a FeatureGet schema from Bitrix24 feature.get data.

        Args:
            bitrix_data: Raw ``result`` object returned by the ``feature.get`` method.

        Returns:
            FeatureGet schema with Python-friendly field names and types.
        """
        return cls(
            value=bool_from_bitrix(bitrix_data["value"], is_required=True),
            lang_selfhosted=bitrix_data.get("lang_selfhosted"),
        )

    def to_bitrix(self) -> FeatureGetData:
        """
        Convert the schema back to a Bitrix-compatible dictionary.

        Returns:
            Dictionary with Bitrix24 field names.
        """

        bitrix_data: FeatureGetData = {
            "value": bool_to_bitrix(self.value, is_required=True),
        }

        if self.lang_selfhosted is not None:
            bitrix_data["lang_selfhosted"] = self.lang_selfhosted

        return bitrix_data
