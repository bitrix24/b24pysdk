from typing import Text

from ....api.requests import BitrixAPIRequest
from ....utils.functional import classproperty, type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "File",
]


class File(BaseEntity):
    """Class for managing files in chats.

    Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/im.v2/files/index.html
    """

    @classproperty
    def _name(cls) -> Text:
        """"""
        return "File"

    @type_checker
    def download(
            self,
            dialog_id: Text,
            file_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a link to download a file

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/im.v2/files/file-download.html

        The method returns a link to download a file from the chat.

        Args:
            dialog_id: ID for the dialog;

            file_id: ID of the file on Drive;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "dialogId": dialog_id,
            "fileId": file_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.download,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def upload(
            self,
            dialog_id: Text,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Upload file

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/im.v2/files/file-upload.html

        The method uploads a file to the chat on behalf of the current user.

        Args:
            dialog_id: ID of the dialog;

            fields: Object with file and message parameters;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "dialogId": dialog_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.upload,
            params=params,
            timeout=timeout,
        )
