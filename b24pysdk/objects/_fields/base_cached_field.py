from abc import ABC
from typing import TYPE_CHECKING, Any, Generic, Text

from ..._constants import MISSING
from ...utils.type_vars import BRawT, BValueT
from .base_field import BaseField

if TYPE_CHECKING:
    from .._base_object import BaseObject

__all__ = [
    "BaseCachedField",
]


class BaseCachedField(BaseField[BRawT, BValueT], ABC, Generic[BRawT, BValueT]):
    """Abstract base field descriptor with an instance-level value cache."""

    __slots__ = ()

    def _get_cache_attr_name(self, instance: "BaseObject") -> Text:
        """Return the private instance attribute name used for this field cache."""
        return f"_{instance.__class__.__name__}__{self.attr_name}"

    def get_cached_value(self, instance: "BaseObject") -> Any:
        """Return the cached field value or ``MISSING`` when no cache exists."""
        return getattr(instance, self._get_cache_attr_name(instance), MISSING)

    def set_cached_value(self, instance: "BaseObject", value: Any):
        """Store a converted field value in the instance cache."""
        setattr(instance, self._get_cache_attr_name(instance), value)

    def delete_cached_value(self, instance: "BaseObject"):
        """Delete the cached field value, if it exists."""
        instance.__dict__.pop(self._get_cache_attr_name(instance), None)
