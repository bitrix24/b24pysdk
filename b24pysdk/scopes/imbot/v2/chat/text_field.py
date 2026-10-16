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
    """Class for managing availability of text field.

    Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/ui/index.html
    """

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
        """Managing the text input field

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/ui/chat-text-field-enabled.html

        The method enables the text input field in the chat.

        Args:
            bot_id: Bot ID;

            dialog_id: Dialog ID;

            bot_token: Unique authorization bot token;

            enabled: Control the input field;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

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
