from dataclasses import dataclass
from typing import Annotated, Dict, Optional, Text, TypedDict

from ...constants.crm import CurrencyThousandsVariant
from ...utils.converters import (
    bool_from_bitrix,
    bool_to_bitrix,
    int_from_bitrix,
    int_to_bitrix,
    text_from_bitrix,
    text_to_bitrix,
)
from ...utils.dataclasses import frozen_dataclass_kwargs
from ...utils.types import B24BoolStrictLiteral
from .._base_schema import BaseSchema
from .._base_schema_dict import BaseSchemaDict

__all__ = [
    "CurrencyLocalization",
    "CurrencyLocalizationData",
    "CurrencyLocalizationsData",
    "CurrencyLocalizationsDict",
]


class CurrencyLocalizationData(TypedDict):
    FORMAT_STRING: Text
    FULL_NAME: Text
    DEC_POINT: Text
    THOUSANDS_SEP: Optional[Text]
    DECIMALS: int
    THOUSANDS_VARIANT: Text
    HIDE_ZERO: Annotated[Text, B24BoolStrictLiteral]


CurrencyLocalizationsData = Dict[Text, CurrencyLocalizationData]


@dataclass(**frozen_dataclass_kwargs())
class CurrencyLocalization(BaseSchema[CurrencyLocalizationData]):
    """Single currency localization returned by ``crm.currency.localizations.get``."""

    format_string: Text
    full_name: Text
    dec_point: Text
    thousands_sep: Optional[Text]
    decimals: int
    thousands_variant: CurrencyThousandsVariant
    hide_zero: bool

    @classmethod
    def from_bitrix(cls, bitrix_data: CurrencyLocalizationData, /) -> "CurrencyLocalization":
        """Create a currency localization schema from Bitrix24 data."""
        return cls(
            format_string=text_from_bitrix(bitrix_data["FORMAT_STRING"], is_required=True),
            full_name=text_from_bitrix(bitrix_data["FULL_NAME"], is_required=True),
            dec_point=text_from_bitrix(bitrix_data["DEC_POINT"], is_required=True),
            thousands_sep=text_from_bitrix(bitrix_data["THOUSANDS_SEP"]),
            decimals=int_from_bitrix(bitrix_data["DECIMALS"], is_required=True),
            thousands_variant=CurrencyThousandsVariant(bitrix_data["THOUSANDS_VARIANT"]),
            hide_zero=bool_from_bitrix(bitrix_data["HIDE_ZERO"], is_required=True),
        )

    def to_bitrix(self) -> CurrencyLocalizationData:
        """Convert the schema back to a Bitrix-compatible dictionary."""
        return {
            "FORMAT_STRING": text_to_bitrix(self.format_string, is_required=True),
            "FULL_NAME": text_to_bitrix(self.full_name, is_required=True),
            "DEC_POINT": text_to_bitrix(self.dec_point, is_required=True),
            "THOUSANDS_SEP": text_to_bitrix(self.thousands_sep),
            "DECIMALS": int_to_bitrix(self.decimals, is_required=True),
            "THOUSANDS_VARIANT": self.thousands_variant.value,
            "HIDE_ZERO": bool_to_bitrix(self.hide_zero, is_required=True),
        }


class CurrencyLocalizationsDict(BaseSchemaDict[CurrencyLocalization, CurrencyLocalizationData]):
    """Currency localizations indexed by language identifier."""
    _VALUE_SCHEMA = CurrencyLocalization
