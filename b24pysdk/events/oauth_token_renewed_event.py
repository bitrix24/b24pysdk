from dataclasses import dataclass
from typing import TYPE_CHECKING

from .._constants import PYTHON_VERSION
from .base_bitrix_event import BaseBitrixEvent

if TYPE_CHECKING:
    from ..credentials import RenewedOAuth

__all__ = [
    "OAuthTokenRenewedEvent",
]

_DATACLASS_KWARGS = {"eq": False, "frozen": True}

if PYTHON_VERSION >= (3, 10):
    _DATACLASS_KWARGS["slots"] = True


@dataclass(**_DATACLASS_KWARGS)
class OAuthTokenRenewedEvent(BaseBitrixEvent):
    """"""
    renewed_oauth_token: "RenewedOAuth"
