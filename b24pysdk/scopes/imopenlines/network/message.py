from typing import Optional, Text, Union

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.converters import bool_to_bitrix
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Message",
]


class Message(BaseEntity):
    """Class for sending messages on behalf of the open channel.

    Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/index.html
    """

    @type_checker
    def add(
            self,
            code: Text,
            user_id: Union[int, Text],
            message: Text,
            *,
            attach: Optional[JSONDict] = MISSING,
            keyboard: Optional[JSONDict] = MISSING,
            url_preview: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Send a message to a user on behalf of thee open channel

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/imopenlines-network-message-add.html

        The method sends a message to a user on bahalf of the open channel connected in Bitrix24 Network.

        Args:
            code: Code of the open channel, a string of 32 characters;

            user_id: Identifier of the message recipient;

            message: Text of the message;

            attach: Attachment;

            keyboard: Keyboard;

            url_preview: Link preview;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            CODE=code,
            USER_ID=user_id,
            MESSAGE=message,
        )

        if attach is not MISSING:
            params["ATTACH"] = attach

        if keyboard is not MISSING:
            params["KEYBOARD"] = keyboard

        if url_preview is not MISSING:
            params["URL_PREVIEW"] = bool_to_bitrix(url_preview, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )
