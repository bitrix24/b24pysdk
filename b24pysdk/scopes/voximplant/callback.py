from typing import Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Callback",
]


class Callback(BaseEntity):
    """Class for managing callbacks.

    Documentation: https://apidocs.bitrix24.com/api-reference/telephony/voximplant/index.html
    """

    @type_checker
    def start(
            self,
            from_line: Text,
            to_number: Text,
            text_to_pronounce: Text,
            *,
            voice: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Start a callback

        Documentation: https://apidocs.bitrix24.com/api-reference/telephony/voximplant/voximplant-callback-start.html

        The method initiates a callback between an employee and a client.

        Args:
            from_line: Identifier of the outgoing line from which the callback is initiated;

            to_number: The client's number to call;

            text_to_pronounce: The text that the system will pronounce to the employee before connecting with the client;

            voice: Identifier of the voice for speech synthesis;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "FROM_LINE": from_line,
            "TO_NUMBER": to_number,
            "TEXT_TO_PRONOUNCE": text_to_pronounce,
        }

        if voice is not MISSING:
            params["VOICE"] = voice

        return self._make_bitrix_api_request(
            api_wrapper=self.start,
            params=params,
            timeout=timeout,
        )
