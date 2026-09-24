from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Url",
]


class Url(BaseEntity):
    """Class for retrieving telephony pages.

    Documentation: https://apidocs.bitrix24.com/api-reference/telephony/voximplant/index.html
    """

    @type_checker
    def get(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get links for navigation in the telephony pages

        Documentation: https://apidocs.bitrix24.com/api-reference/telephony/voximplant/voximplant-url-get.html

        The method returns links for navigation in the telephony pages.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            timeout=timeout,
        )
