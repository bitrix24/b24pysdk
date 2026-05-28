from dataclasses import dataclass
from typing import Text

from .._constants import PYTHON_VERSION
from .base_bitrix_event import BaseBitrixEvent

__all__ = [
    "PortalDomainChangedEvent",
]

_DATACLASS_KWARGS = {"eq": False, "frozen": True}

if PYTHON_VERSION >= (3, 10):
    _DATACLASS_KWARGS["slots"] = True


@dataclass(**_DATACLASS_KWARGS)
class PortalDomainChangedEvent(BaseBitrixEvent):
    """
    Event emitted when a Bitrix24 portal domain changes.

    Attributes:
        old_domain: Previous portal domain.
        new_domain: Updated portal domain.
    """

    old_domain: Text
    new_domain: Text
