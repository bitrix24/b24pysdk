from typing import Optional, Text

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import classproperty, type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "TextField",
]


class TextField(BaseEntity):
    """"""

    @classproperty
    def _name(cls) -> Text:
        """"""
        return "TextField"

    @type_checker
    def enabled(
            self,
            bot_id: int,
            dialog_id: Text,
            *,
            bot_token: Optional[Text] = MISSING,
            enabled: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "botId": bot_id,
            "dialogId": dialog_id,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        if enabled is not MISSING:
            params["enabled"] = enabled

        return self._make_bitrix_api_request(
            api_wrapper=self.enabled,
            params=params,
            timeout=timeout,
        )
