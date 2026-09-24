from abc import ABC
from types import MappingProxyType
from typing import TYPE_CHECKING, Any, ClassVar, Final, Mapping, Text, Type

from ..utils.enum import StrEnum

if TYPE_CHECKING:
    from ._fields.base_field import BaseField

__all__ = [
    "BASIC_FILTER_OPERATORS",
    "NO_FILTER_OPERATORS",
    "ORDERED_FILTER_OPERATORS",
    "TEXT_FILTER_OPERATORS",
    "BaseFilterOperator",
    "ContainsFilterOperator",
    "FilterLookup",
    "GreaterThanFilterOperator",
    "GreaterThanOrEqualFilterOperator",
    "InFilterOperator",
    "LessThanFilterOperator",
    "LessThanOrEqualFilterOperator",
    "LikeFilterOperator",
    "NotContainsFilterOperator",
    "NotExactFilterOperator",
    "NotInFilterOperator",
    "NotLikeFilterOperator",
]


class FilterLookup(StrEnum):
    """Named SDK filter lookups supported by Bitrix24 object queries."""
    NOT_EXACT = "ne"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    IN = "in"
    NOT_IN = "not_in"
    CONTAINS = "contains"
    LIKE = "like"
    NOT_CONTAINS = "not_contains"
    NOT_LIKE = "not_like"


class BaseFilterOperator(ABC):
    """Base implementation of a Bitrix24 filter operator."""

    lookup: ClassVar[FilterLookup]
    bitrix_prefix: ClassVar[Text]

    @classmethod
    def prepare_value(cls, bitrix_field: "BaseField[Any, Any]", value: Any) -> Any:
        """Convert a public filter value to its Bitrix24 representation."""
        return bitrix_field.to_bitrix_value(value)


class NotExactFilterOperator(BaseFilterOperator):
    lookup = FilterLookup.NOT_EXACT
    bitrix_prefix = "!="


class GreaterThanFilterOperator(BaseFilterOperator):
    lookup = FilterLookup.GT
    bitrix_prefix = ">"


class GreaterThanOrEqualFilterOperator(BaseFilterOperator):
    lookup = FilterLookup.GTE
    bitrix_prefix = ">="


class LessThanFilterOperator(BaseFilterOperator):
    lookup = FilterLookup.LT
    bitrix_prefix = "<"


class LessThanOrEqualFilterOperator(BaseFilterOperator):
    lookup = FilterLookup.LTE
    bitrix_prefix = "<="


class InFilterOperator(BaseFilterOperator):
    lookup = FilterLookup.IN
    bitrix_prefix = "@"

    @classmethod
    def prepare_value(cls, bitrix_field: "BaseField[Any, Any]", value: Any) -> Any:
        """Validate and convert an iterable for a Bitrix24 ``IN`` lookup.

        For a scalar field, each candidate is converted independently and the
        resulting list is used as the filter value. For a multiple field, the
        iterable represents that field's public multiple value and is converted
        by the descriptor as a whole. Strings, mappings, and other unsupported
        pseudo-iterables are rejected by ``BaseField.is_iterable()``.
        """

        if not bitrix_field.is_iterable(value):
            raise TypeError(
                f"Filter lookup {cls.lookup.value!r} for field "
                f"{bitrix_field.attr_name!r} expects an iterable value.",
            )

        if bitrix_field.is_multiple:
            return bitrix_field.to_bitrix_value(value)

        return [bitrix_field.to_bitrix_value(item) for item in value]


class NotInFilterOperator(InFilterOperator):
    lookup = FilterLookup.NOT_IN
    bitrix_prefix = "!@"


class ContainsFilterOperator(BaseFilterOperator):
    lookup = FilterLookup.CONTAINS
    bitrix_prefix = "%"


class LikeFilterOperator(BaseFilterOperator):
    lookup = FilterLookup.LIKE
    bitrix_prefix = "=%"


class NotContainsFilterOperator(BaseFilterOperator):
    lookup = FilterLookup.NOT_CONTAINS
    bitrix_prefix = "!%"


class NotLikeFilterOperator(BaseFilterOperator):
    lookup = FilterLookup.NOT_LIKE
    bitrix_prefix = "!=%"


BASIC_FILTER_OPERATORS: Final[Mapping[FilterLookup, Type[BaseFilterOperator]]] = MappingProxyType({
    FilterLookup.NOT_EXACT: NotExactFilterOperator,
    FilterLookup.IN: InFilterOperator,
    FilterLookup.NOT_IN: NotInFilterOperator,
})

ORDERED_FILTER_OPERATORS: Final[Mapping[FilterLookup, Type[BaseFilterOperator]]] = MappingProxyType({
    **BASIC_FILTER_OPERATORS,
    FilterLookup.GT: GreaterThanFilterOperator,
    FilterLookup.GTE: GreaterThanOrEqualFilterOperator,
    FilterLookup.LT: LessThanFilterOperator,
    FilterLookup.LTE: LessThanOrEqualFilterOperator,
})

TEXT_FILTER_OPERATORS: Final[Mapping[FilterLookup, Type[BaseFilterOperator]]] = MappingProxyType({
    **BASIC_FILTER_OPERATORS,
    FilterLookup.CONTAINS: ContainsFilterOperator,
    FilterLookup.LIKE: LikeFilterOperator,
    FilterLookup.NOT_CONTAINS: NotContainsFilterOperator,
    FilterLookup.NOT_LIKE: NotLikeFilterOperator,
})

NO_FILTER_OPERATORS: Final[Mapping[FilterLookup, Type[BaseFilterOperator]]] = MappingProxyType({})
