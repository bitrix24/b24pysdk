from dataclasses import dataclass
from typing import Text

from .base_bitrix_event import BaseBitrixEvent


@dataclass
class AuthTokenRenewedEvent(BaseBitrixEvent):
    """"""

    auth_token: Text
    refresh_token: Text
