from dataclasses import dataclass

from ..utils.dataclasses import frozen_dataclass_kwargs

__all__ = [
    "BaseBitrixEvent",
]


@dataclass(**frozen_dataclass_kwargs(eq=False))
class BaseBitrixEvent:
    """
    Base class for SDK events.

    Used as a common parent for all events emitted by the Bitrix24 SDK.
    """
