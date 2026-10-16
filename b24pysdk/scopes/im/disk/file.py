from typing import Optional, Text, Union

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.converters import bool_to_bitrix
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "File",
]


class File(BaseEntity):
    """Class for managing files in chats.

    Documentation: https://apidocs.bitrix24.com/api-reference/chats/files/index.html
    """

    @type_checker
    def commit(
            self,
            *,
            chat_id: Union[int, Text] = MISSING,
            dialog_id: Text = MISSING,
            upload_id: Union[int, Text] = MISSING,
            file_id: Union[int, Text] = MISSING,
            message: Optional[Text] = MISSING,
            silent_mode: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """Add file to chat

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/files/im-disk-file-commit.html

        The method adds a file to chat.

        Args:
            chat_id: Chat identifier, required if dialog_id is not provided;

            dialog_id: Dialog identifier, required if chat_id is not provided;

            upload_id: Upload identifier, required if file_id is not provided;

            file_id: File identifier, required if upload_id is not provided;

            message: Text message with the file;

            silent_mode: Parameter for Open Channels chat;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if chat_id is not MISSING:
            params["CHAT_ID"] = chat_id

        if dialog_id is not MISSING:
            params["DIALOG_ID"] = dialog_id

        if upload_id is not MISSING:
            params["UPLOAD_ID"] = upload_id

        if file_id is not MISSING:
            params["FILE_ID"] = file_id

        if message is not MISSING:
            params["MESSAGE"] = message

        if silent_mode is not MISSING:
            params["SILENT_MODE"] = bool_to_bitrix(silent_mode, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self.commit,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            chat_id: Union[int, Text],
            file_id: Union[int, Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Delete file from chat folder

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/files/im-disk-file-delete.html

        The method removes a file from the chat folder.

        Args:
            chat_id: Chat identifier;

            file_id: Identifier of the file;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "CHAT_ID": chat_id,
            "FILE_ID": file_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def save(
            self,
            file_id: Union[int, Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """Save file to your Drive

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/files/im-disk-file-save.html

        The method saves a file from the chat to the user's personal Drive.

        Args:
            file_id: Identifier of the file;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "FILE_ID": file_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.save,
            params=params,
            timeout=timeout,
        )
