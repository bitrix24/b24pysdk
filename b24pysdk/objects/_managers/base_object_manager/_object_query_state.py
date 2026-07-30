from dataclasses import dataclass, replace
from typing import Iterable, Optional, Text, Tuple

from ....utils.dataclasses import frozen_dataclass_kwargs
from ....utils.types import DefaultTimeout, JSONDict, Timeout

__all__ = [
    "ObjectQueryState",
]


@dataclass(**frozen_dataclass_kwargs())
class ObjectQueryState:
    """Immutable configuration of one object-manager query."""

    filter_param: Optional[JSONDict] = None
    order_param: Optional[JSONDict] = None
    select_param: Optional[Tuple[Text, ...]] = None
    kwargs: Optional[JSONDict] = None
    limit_param: Optional[int] = None
    start_param: Optional[int] = None
    timeout: Timeout = None
    is_fast: bool = False
    is_reversed: bool = False
    is_result_query: bool = False

    def __post_init__(self):
        """Copy mutable query parameters stored in the frozen state."""

        if self.filter_param is not None:
            object.__setattr__(self, "filter_param", dict(self.filter_param))

        if self.order_param is not None:
            object.__setattr__(self, "order_param", dict(self.order_param))

        if self.select_param is not None:
            object.__setattr__(self, "select_param", tuple(self.select_param))

        if self.kwargs is not None:
            object.__setattr__(self, "kwargs", dict(self.kwargs))

    def with_filter_param(self, filter_param: Optional[JSONDict]) -> "ObjectQueryState":
        """Return a copy with filtering parameters replaced."""
        return replace(
            self,
            filter_param=filter_param,
            is_result_query=True,
        )

    def with_order_param(self, order_param: Optional[JSONDict]) -> "ObjectQueryState":
        """Return a copy with ordering parameters replaced."""
        return replace(
            self,
            order_param=order_param,
            is_result_query=True,
        )

    def with_select_param(self, select_param: Optional[Iterable[Text]]) -> "ObjectQueryState":
        """Return a copy with selected field codes replaced."""
        return replace(
            self,
            select_param=tuple(select_param) if select_param is not None else None,
            is_result_query=True,
        )

    def with_kwargs(self, kwargs: Optional[JSONDict]) -> "ObjectQueryState":
        """Return a copy with additional request parameters replaced."""
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
