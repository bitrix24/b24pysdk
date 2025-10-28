from abc import ABC

from ._base_context import BaseContext


class BaseEntity(BaseContext, ABC):
    """"""

    __slots__ = ("_context",)

    _context: BaseContext

    def __init__(self, context: BaseContext):
        self._context = context

    def __repr__(self):
        return f"client.{self}"
