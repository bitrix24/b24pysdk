from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, Any, Dict, Iterable, Optional, Text, Tuple, Type

from ....utils.dataclasses import frozen_dataclass_kwargs
from ....utils.types import DefaultTimeout, JSONDict, Timeout
from ..._fields.object_field import ObjectField
from ...errors import BitrixObjectFieldError

if TYPE_CHECKING:
    from ..._base_object import BaseObject

__all__ = [
    "ObjectQueryState",
    "SelectParam",
]


# Keys are Bitrix24 field codes. ``None`` marks a terminal ordinary field,
# while a nested mapping follows an ObjectField; an empty mapping marks a
# terminal ObjectField.
SelectParam = Dict[Text, Optional["SelectParam"]]


def _copy_select_param(select_param: Optional[SelectParam]) -> SelectParam:
    """Recursively copy a selection tree owned by another query state."""

    if select_param is None:
        return {}

    return {
        bitrix_code: None if nested_param is None else _copy_select_param(nested_param)
        for bitrix_code, nested_param in select_param.items()
    }


def _get_nested_select_param(select_param: SelectParam, bitrix_codes: Iterable[Text]) -> SelectParam:
    """Create a nested code path when necessary and return its leaf mapping."""

    nested_param = select_param

    for bitrix_code in bitrix_codes:
        next_nested_param = nested_param.get(bitrix_code)

        if next_nested_param is None:
            next_nested_param = {}
            nested_param[bitrix_code] = next_nested_param

        nested_param = next_nested_param

    return nested_param


def _resolve_select_path(
        object_class: "Type[BaseObject[Any]]",
        field_path: Text,
) -> Tuple[Tuple[Text, ...], Tuple[Text, ...]]:
    """Resolve one ``select()`` path to relation codes and terminal field codes."""

    if not field_path:
        raise BitrixObjectFieldError("Select field name cannot be empty.")

    attr_names = field_path.split(".")
    current_object_class = object_class
    relation_bitrix_codes = []

    for index, attr_name in enumerate(attr_names):
        if not attr_name:
            raise BitrixObjectFieldError(f"Invalid select field path {field_path!r}.")

        object_meta = current_object_class.get_meta()
        is_last = index == len(attr_names) - 1

        if attr_name == "bitrix_pk":
            if not is_last:
                raise BitrixObjectFieldError(
                    f"Field {attr_name!r} on {current_object_class.__name__} is not an ObjectField.",
                )

            return tuple(relation_bitrix_codes), object_meta.pk_bitrix_codes

        bitrix_field = object_meta.get_field(attr_name)

        if is_last:
            return tuple(relation_bitrix_codes), object_meta.get_bitrix_codes_by_attr_name(attr_name)

        if not isinstance(bitrix_field, ObjectField):
            raise BitrixObjectFieldError(
                f"Field {attr_name!r} on {current_object_class.__name__} is not an ObjectField.",
            )

        relation_bitrix_codes.append(bitrix_field.bitrix_code)
        current_object_class = bitrix_field.object_class

    raise BitrixObjectFieldError(f"Invalid select field path {field_path!r}.")


def _resolve_select_related_path(
        object_class: "Type[BaseObject[Any]]",
        field_path: Text,
) -> Tuple[Tuple[Text, ...], Optional[Tuple[Text, ...]]]:
    """Resolve one related path and optional terminal fields in a single pass."""

    if not field_path:
        raise BitrixObjectFieldError("Related field name cannot be empty.")

    attr_names = field_path.split(".")
    current_object_class = object_class
    relation_bitrix_codes = []

    for index, attr_name in enumerate(attr_names):
        if not attr_name:
            raise BitrixObjectFieldError(f"Invalid related field path {field_path!r}.")

        if attr_name == "bitrix_pk":
            raise BitrixObjectFieldError(
                f"Field {attr_name!r} on {current_object_class.__name__} is not an ObjectField.",
            )

        object_meta = current_object_class.get_meta()
        bitrix_field = object_meta.get_field(attr_name)
        is_last = index == len(attr_names) - 1

        if isinstance(bitrix_field, ObjectField):
            relation_bitrix_codes.append(bitrix_field.bitrix_code)
            current_object_class = bitrix_field.object_class

            if is_last:
                return tuple(relation_bitrix_codes), None

            continue

        if not is_last or not relation_bitrix_codes:
            raise BitrixObjectFieldError(
                f"Field {attr_name!r} on {current_object_class.__name__} is not an ObjectField.",
            )

        return tuple(relation_bitrix_codes), object_meta.get_bitrix_codes_by_attr_name(attr_name)

    raise BitrixObjectFieldError(f"Invalid related field path {field_path!r}.")


def _get_updated_select_param(
        object_class: "Type[BaseObject[Any]]",
        current_select_param: Optional[SelectParam],
        field_paths: Iterable[Text],
) -> SelectParam:
    """Return a copied selection tree containing the requested field paths."""

    select_param = _copy_select_param(current_select_param)

    for field_path in field_paths:
        relation_bitrix_codes, terminal_bitrix_codes = _resolve_select_path(object_class, field_path)
        nested_param = _get_nested_select_param(select_param, relation_bitrix_codes)

        for bitrix_code in terminal_bitrix_codes:
            if bitrix_code not in nested_param:
                nested_param[bitrix_code] = None

    return select_param


def _get_updated_select_related_param(
        object_class: "Type[BaseObject[Any]]",
        current_select_related_param: Optional[SelectParam],
        field_paths: Iterable[Text],
) -> SelectParam:
    """Return a copied relation tree containing paths and terminal fields."""

    select_related_param = _copy_select_param(current_select_related_param)

    for field_path in field_paths:
        relation_bitrix_codes, terminal_bitrix_codes = _resolve_select_related_path(object_class, field_path)
        relation_param = _get_nested_select_param(select_related_param, relation_bitrix_codes)

        if terminal_bitrix_codes is None:
            continue

        for bitrix_code in terminal_bitrix_codes:
            relation_param.setdefault(bitrix_code)

    return select_related_param


@dataclass(**frozen_dataclass_kwargs(eq=False))
class ObjectQueryState:
    """Shallowly immutable configuration of one object-manager query.

    Manager query methods never mutate an existing state. Each ``with_*``
    method uses :func:`dataclasses.replace` and returns a new instance, allowing
    the original manager and all of its clones to be evaluated independently.

    The dataclass is frozen, but mapping fields are not deeply immutable. They
    are owned by the query-building code and treated as read-only after being
    assigned. Consequently, unchanged mappings may be shared safely between
    manager clones without repeated defensive copies. Methods that modify a
    mapping first build a new one; selection updates do that recursively in
    :func:`_get_updated_select_param` and
    :func:`_get_updated_select_related_param`.

    ``is_result_query`` distinguishes an unexecuted descriptor/builder from a
    query that may be evaluated. Execution-specific data, including a cached
    response, lives on the manager rather than in this reusable state object.
    """

    filter_param: Optional[JSONDict] = None
    order_param: Optional[JSONDict] = None
    select_param: Optional[SelectParam] = None
    select_related_param: Optional[SelectParam] = None
    kwargs: Optional[JSONDict] = None
    limit_param: Optional[int] = None
    start_param: Optional[int] = None
    timeout: Timeout = None
    is_fast: bool = False
    is_reversed: bool = False
    is_result_query: bool = False

    def with_filter_param(self, filter_param: Optional[JSONDict]) -> "ObjectQueryState":
        """Return a copy with filtering parameters replaced.

        The internally owned mapping is stored by reference and becomes
        read-only once attached to the state.
        """
        return replace(
            self,
            filter_param=filter_param,
            is_result_query=True,
        )

    def with_order_param(self, order_param: Optional[JSONDict]) -> "ObjectQueryState":
        """Return a copy with ordering parameters replaced.

        The internally owned mapping is stored by reference and becomes
        read-only once attached to the state.
        """
        return replace(self, order_param=order_param)

    def with_updated_select_param(
            self,
            object_class: "Type[BaseObject[Any]]",
            field_paths: Iterable[Text],
    ) -> "ObjectQueryState":
        """Return a state with ordinary selected-field paths merged into a new tree."""

        updated_select_param = _get_updated_select_param(
            object_class,
            self.select_param,
            field_paths,
        )

        return replace(self, select_param=updated_select_param)

    def with_updated_select_related_param(
            self,
            object_class: "Type[BaseObject[Any]]",
            field_paths: Iterable[Text],
    ) -> "ObjectQueryState":
        """Return a state with related paths and their terminal selections merged."""

        updated_select_related_param = _get_updated_select_related_param(
            object_class,
            self.select_related_param,
            field_paths,
        )

        return replace(self, select_related_param=updated_select_related_param)

    def with_select_param(self, select_param: Optional[SelectParam]) -> "ObjectQueryState":
        """Return a copy with the selected-field tree replaced.

        The mapping reference is stored as-is. This internal method is intended
        for a tree that is already owned by query-building code and will remain
        read-only after assignment.
        """
        return replace(self, select_param=select_param)

    def with_select_related_param(self, select_related_param: Optional[SelectParam]) -> "ObjectQueryState":
        """Return a copy with the related-field tree replaced.

        The mapping reference is stored as-is. Callers must pass an internally
        owned tree and must not mutate it after attaching it to the state.
        """
        return replace(self, select_related_param=select_related_param)

    def with_kwargs(self, kwargs: Optional[JSONDict]) -> "ObjectQueryState":
        """Return a copy with additional request parameters replaced.

        The internally owned top-level mapping is stored by reference. Query
        builders copy it before adding or replacing request parameters.
        """
        return replace(
            self,
            kwargs=kwargs,
            is_result_query=True,
        )

    def with_limit_param(self, limit_param: Optional[int]) -> "ObjectQueryState":
        """Return a copy with the result limit replaced."""
        return replace(
            self,
            limit_param=limit_param,
            is_result_query=True,
        )

    def with_start_param(self, start_param: Optional[int]) -> "ObjectQueryState":
        """Return a copy with the pagination offset replaced."""
        return replace(
            self,
            start_param=start_param,
            is_result_query=True,
        )

    def with_timeout(self, timeout: DefaultTimeout) -> "ObjectQueryState":
        """Return a copy with the request timeout replaced."""
        return replace(self, timeout=timeout)

    def with_is_fast(self, is_fast: bool) -> "ObjectQueryState":
        """Return a copy with the fast-loading flag replaced."""
        return replace(self, is_fast=is_fast)

    def with_is_reversed(self, is_reversed: bool) -> "ObjectQueryState":
        """Return a copy with the reverse-order flag replaced."""
        return replace(
            self,
            is_reversed=is_reversed,
            is_result_query=True,
        )

    def with_is_result_query(self, is_result_query: bool) -> "ObjectQueryState":
        """Return a copy with the executable-query flag replaced."""
        return replace(self, is_result_query=is_result_query)
