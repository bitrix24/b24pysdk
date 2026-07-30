from typing import Optional, Text

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import classproperty, type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "InputAction",
]


class InputAction(BaseEntity):
    """"""

    @classproperty
    def _name(cls) -> Text:
        """"""
        return "InputAction"

    @type_checker
    def notify(
            self,
            bot_id: int,
            dialog_id: Text,
            *,
            bot_token: Optional[Text] = MISSING,
            status_message_code: Optional[Text] = MISSING,
            duration: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "botId": bot_id,
            "dialogId": dialog_id,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        if status_message_code is not MISSING:
            params["statusMessageCode"] = status_message_code

        if duration is not MISSING:
            params["duration"] = duration

        return self._make_bitrix_api_request(
            api_wrapper=self.notify,
            params=params,
            timeout=timeout,
        )
