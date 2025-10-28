from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..._constants import PYTHON_VERSION as _PV
from .base_bitrix_event import BaseBitrixEvent

if TYPE_CHECKING:
    from ..credentials import RenewedOAuthToken

_DATACLASS_KWARGS = {"eq": False, "frozen": True}

if _PV >= (3, 10):
    _DATACLASS_KWARGS["slots"] = True


@dataclass(**_DATACLASS_KWARGS)
class OAuthTokenRenewedEvent(BaseBitrixEvent):
    """"""
    renewed_oauth_token: "RenewedOAuthToken"
