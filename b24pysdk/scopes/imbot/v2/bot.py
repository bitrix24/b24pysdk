from typing import Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import classproperty, type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Bot",
]


class Bot(BaseEntity):
    """Class for managing lifecycle of a chatbot.

    Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/bots/index.html
    """

    @classproperty
    def _name(cls) -> Text:
        """"""
        return "Bot"

    @type_checker
    def get(
            self,
            *,
            bot_id: Optional[int] = MISSING,
            code: Optional[Text] = MISSING,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get information about the bot

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/bots/bot-get.html

        The method returns information about the bot.

        Args:
            bot_id: Bot ID;

            code: Bot code;

            bot_token: Unique authorization bot token;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if bot_id is not MISSING:
            params["botId"] = bot_id

        if code is not MISSING:
            params["code"] = code

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            bot_token: Optional[Text] = MISSING,
            filter: Optional[JSONDict] = MISSING,
            limit: Optional[int] = MISSING,
            offset: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """List of application bots

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/bots/bot-list.html

        The method returns a list of bots for the current application in an extended format.

        Args:
            bot_token: Unique authorization bot token;

            filter: Parameter for filtering;

            limit: Number of records;

            offset: Offset for pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        if filter is not MISSING:
            params["filter"] = filter

        if limit is not MISSING:
            params["limit"] = limit

        if offset is not MISSING:
            params["offset"] = offset

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def register(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Register a bot

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/bots/bot-register.html

        The method register a new chat bot.

        Args:
            fields: Object with bot parameters;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.register,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unregister(
            self,
            bot_id: int,
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Unregister a bot

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/bots/bot-unregister.html

        The method deletes the bot.

        Args:
            bot_id: Bor ID;

            bot_token: Unique authorization bot token;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "botId": bot_id,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        return self._make_bitrix_api_request(
            api_wrapper=self.unregister,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            bot_id: int,
            fields: JSONDict,
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update a bot

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/bots/bot-update.html

        The method updates the properties of the bot.

        Args:
            bot_id: Bor ID;

            fields: Object with bot parameters to be updated;

            bot_token: Unique authorization bot token;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "botId": bot_id,
            "fields": fields,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
