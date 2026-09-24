from typing import Optional

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Agreement",
]


class Agreement(BaseEntity):
    """Class for retrieving user agreements.

    Documentation: https://apidocs.bitrix24.com/api-reference/user-consent/index.html
    """

    @type_checker
    def list(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of agreements

        Documentation: https://apidocs.bitrix24.com/api-reference/user-consent/user-consent-agreement-list.html

        The method returns a list of agreements.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            timeout=timeout,
        )

    @type_checker
    def text(
            self,
            bitrix_id: int,
            *,
            replace: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the text of the agreement

        Documentation: https://apidocs.bitrix24.com/api-reference/user-consent/user-consent-agreement-text.html

        The method returns the text of the agreement.

        Args:
            bitrix_id: Identifier of the agreement;

            replace: Array of replacements for text substitution;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
        }

        if replace is not MISSING:
            params["replace"] = replace

        return self._make_bitrix_api_request(
            api_wrapper=self.text,
            params=params or None,
            timeout=timeout,
        )
