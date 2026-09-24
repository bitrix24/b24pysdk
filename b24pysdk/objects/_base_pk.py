from abc import ABC, abstractmethod
from collections.abc import Hashable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Text

from ..schemas._base_schema import BaseSchema
from ..utils.dataclasses import frozen_dataclass_kwargs
from ..utils.types import JSONDict

__all__ = [
    "BasePK",
]


@dataclass(**frozen_dataclass_kwargs())
class BasePK(BaseSchema[JSONDict], ABC, Hashable):
    """Base class for immutable composite primary-key schemas.

    Subclasses expose Python-friendly key components through dataclass fields
    and implement conversion from and to the raw Bitrix24 key dictionary.
    Frozen dataclass semantics make their instances safe to use as object
    identifiers and dictionary keys.
    """

    if TYPE_CHECKING:
        def __hash__(self) -> int: ...

    @abstractmethod
    def __post_init__(self):
        """Validate and normalize values passed to the dataclass constructor.

        Implementations may convert supported raw Bitrix24 scalar values and
        store the converted result through ``_set_value()``. Unsupported values
        must raise ``TypeError`` or ``ValueError``.
        """
        raise NotImplementedError

    def _set_value(self, attr_name: Text, value: Any, /):
        """Set a normalized dataclass field during ``__post_init__``.

        Composite keys are frozen and hashable after construction. This helper
        is intended only for normalization performed from a subclass
        ``__post_init__`` implementation.
        """

        if attr_name not in self.__dataclass_fields__:
            raise AttributeError(
                f"{self.__class__.__name__} has no dataclass field {attr_name!r}.",
            )

        object.__setattr__(self, attr_name, value)
