from typing import Any, Optional

from .._filter_lookups import NO_FILTER_OPERATORS
from .base_field import BaseField

__all__ = [
    "RawField",
]


class RawField(BaseField[Any, Any]):
    """Field that preserves an otherwise undocumented Bitrix24 value.

    Scalar values pass through unchanged, including mutable objects. Conversion
    neither validates their shape nor makes a detached copy. Multiple-value
    container handling is still provided by ``BaseField``.
    """

    _FILTER_OPERATORS = NO_FILTER_OPERATORS

    def _convert_from_bitrix(self, value: Optional[Any]) -> Optional[Any]:
        """Return the raw response value without conversion."""
        return value

    def _convert_to_bitrix(self, value: Optional[Any]) -> Optional[Any]:
        """Return the raw request value without conversion."""
        return value
