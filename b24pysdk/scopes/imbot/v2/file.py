from typing import Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import classproperty, type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "File",
]


class File(BaseEntity):
    """Class for working with files to the chat on behalf of the bot.

    Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/files/index.html
    """

    @classproperty
    def _name(cls) -> Text:
        """"""
        return "File"

    @type_checker
    def download(
            self,
            bot_id: int,
            file_id: int,
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a link to download a file

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/files/file-download.html

        The method returns a link to download a file from the chat.

        Args:
            bot_id: Bot ID;

            file_id: ID of the file on Drive;

            bot_token: Unique authorization token for the bot;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "botId": bot_id,
            "fileId": file_id,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        return self._make_bitrix_api_request(
            api_wrapper=self.download,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def upload(
            self,
            bot_id: int,
            dialog_id: Text,
            fields: JSONDict,
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Upload file

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/files/file-upload.html

        The method uploads a file to the chat on behalf of the current user.

        Args:
            bot_id: Bot ID;

            dialog_id: ID of the dialog;

            fields: Object with file and message parameters;

            bot_token: Unique authorization token for the bot;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest"""

        params: JSONDict = {
            "botId": bot_id,
            "dialogId": dialog_id,
            "fields": fields,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        return self._make_bitrix_api_request(
            api_wrapper=self.upload,
            params=params,
            timeout=timeout,
        )
