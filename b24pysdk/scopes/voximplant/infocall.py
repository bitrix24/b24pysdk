from typing import Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Infocall",
]


class Infocall(BaseEntity):
    """Class for managing auto calls.

    Documentation: https://apidocs.bitrix24.com/api-reference/telephony/voximplant/index.html
    """

    @type_checker
    def startwithsound(
            self,
            from_line: Text,
            to_number: Text,
            url: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Make auto-call with MP3 playback

        Documentation: https://apidocs.bitrix24.com/api-reference/telephony/voximplant/voximplant-infocall-start-with-sound.html

        The method initiates an auto-call and plays an MP3 file from a URL.

        Args:
            from_line: Identifier of the outgoing line from which the call is initiated;

            to_number: The number to which the call should be made;

            url: Link to the MP3 file that should be played during the call;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "FROM_LINE": from_line,
            "TO_NUMBER": to_number,
            "URL": url,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.startwithsound,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def startwithtext(
            self,
            from_line: Text,
            to_number: Text,
            text_to_pronounce: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Initiate an auto-call with the voice automation rule

        Documentation: https://apidocs.bitrix24.com/api-reference/telephony/voximplant/voximplant-infocall-start-with-text.html

        The method initiates an auto-call and plays the specified text to the recipient using speech synthesis.

        Args:
            from_line: Identifier of the outgoing line from which the call is initiated;

            to_number: The number to which the call should be made;

            text_to_pronounce: The text that will be spoken to the recipient;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "FROM_LINE": from_line,
            "TO_NUMBER": to_number,
            "TEXT_TO_PRONOUNCE": text_to_pronounce,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.startwithtext,
            params=params,
            timeout=timeout,
        )
