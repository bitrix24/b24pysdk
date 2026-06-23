from dataclasses import dataclass
from typing import Text

from ..utils.dataclasses import frozen_dataclass_kwargs
from .base_bitrix_event import BaseBitrixEvent

__all__ = [
    "PortalDomainChangedEvent",
]


@dataclass(**frozen_dataclass_kwargs(eq=False))
class PortalDomainChangedEvent(BaseBitrixEvent):
    """
    Event emitted when a Bitrix24 portal domain changes.

    Attributes:
        old_domain: Previous portal domain.
        new_domain: Updated portal domain.
    """
    old_domain: Text
    new_domain: Text
