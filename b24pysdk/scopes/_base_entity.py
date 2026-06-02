from abc import ABC

from ._base_context import BaseContext


class BaseEntity(BaseContext, ABC):
    """
    Base class for nested Bitrix24 API entities.

    Stores a parent context and inherits API path construction, token access,
    and lazy request creation from ``BaseContext``.
    """

    __slots__ = ("_context",)

    _context: BaseContext

    def __init__(self, context: BaseContext):
        """
        Initialize an entity with its parent context.

        Args:
            context: Parent API context from which path, token, and requester
                options are inherited.
        """
        self._context = context

    def __repr__(self):
        return f"client.{self}"
