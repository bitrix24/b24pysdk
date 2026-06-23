from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..utils.dataclasses import frozen_dataclass_kwargs
from .base_bitrix_event import BaseBitrixEvent

if TYPE_CHECKING:
    from ..credentials import RenewedOAuth

__all__ = [
    "OAuthTokenRenewedEvent",
]


@dataclass(**frozen_dataclass_kwargs(eq=False))
class OAuthTokenRenewedEvent(BaseBitrixEvent):
    """
    Event emitted when an OAuth token is renewed.

    Attributes:
        renewed_oauth_token: Newly received OAuth token data.
    """
    renewed_oauth_token: "RenewedOAuth"
