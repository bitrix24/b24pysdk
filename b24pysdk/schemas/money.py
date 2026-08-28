from dataclasses import dataclass
from decimal import ROUND_DOWN, Decimal, InvalidOperation
from typing import Final, Optional, Text

from ..utils.converters import text_from_bitrix, text_to_bitrix
from ..utils.dataclasses import frozen_dataclass_kwargs
from ._base_schema import BaseSchema

__all__ = [
    "Money",
]


_MONEY_PARTS_COUNT: Final[int] = 2
_MONEY_QUANT: Final[Decimal] = Decimal("0.01")


@dataclass(**frozen_dataclass_kwargs())
class Money(BaseSchema[Text]):
    """Structured value of a Bitrix24 money field.

    Bitrix24 stores money as an ``amount|currency`` string, for example
    ``710|RUB``.
    """

    amount: Decimal
    currency: Optional[Text] = None

    @classmethod
    def from_bitrix(cls, bitrix_data: Text, /) -> "Money":
        """Create a money schema from a raw Bitrix24 money string."""

        raw_value = text_from_bitrix(bitrix_data, is_required=True)
        parts = raw_value.rsplit("|", _MONEY_PARTS_COUNT - 1)

        if len(parts) == _MONEY_PARTS_COUNT - 1:
            parts.append("")

        if len(parts) != _MONEY_PARTS_COUNT:
            raise ValueError(
                "Bitrix24 money value must contain amount and optional currency "
                "separated by '|'.",
            )

        amount_value, currency_value = parts

        if not amount_value:
            raise ValueError("Bitrix24 money value must contain amount.")

        try:
            amount = Decimal(amount_value)
        except InvalidOperation as exc:
            raise ValueError(
                f"Bitrix24 money amount {amount_value!r} is not a valid decimal value.",
            ) from exc

        if not amount.is_finite():
            raise ValueError(
                f"Bitrix24 money amount {amount_value!r} must be finite.",
            )

        return cls(
            amount=amount.quantize(_MONEY_QUANT, rounding=ROUND_DOWN),
            currency=text_from_bitrix(currency_value, is_required=True) if currency_value else None,
        )

    def to_bitrix(self) -> Text:
        """Convert the money schema to a Bitrix24 money string."""

        if not isinstance(self.amount, Decimal):
            raise TypeError(
                f"Money amount must be Decimal, got {type(self.amount).__name__}.",
            )

        if not self.amount.is_finite():
            raise ValueError("Money amount must be finite.")

        amount = self.amount.quantize(_MONEY_QUANT, rounding=ROUND_DOWN)

        if self.currency is None:
            return f"{amount}"

        currency = text_to_bitrix(self.currency, is_required=True)

        return f"{amount}|{currency}"
