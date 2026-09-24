from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Voices",
]


class Voices(BaseEntity):
    """Class for retrieving available voices for speech synthesis.

    Documentation: https://apidocs.bitrix24.com/api-reference/telephony/voximplant/index.html
    """

    @type_checker
    def get(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of available voices for text-to-speech

        Documentation: https://apidocs.bitrix24.com/api-reference/telephony/voximplant/voximplant-tts-voices-get.html

        The method returns a list of available voices for text to speech synthesis.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            timeout=timeout,
        )
