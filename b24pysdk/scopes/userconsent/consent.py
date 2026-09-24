from typing import Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Consent",
]


class Consent(BaseEntity):
    """Class for managing user consents.

    Documentation: https://apidocs.bitrix24.com/api-reference/user-consent/index.html
    """

    @type_checker
    def add(
            self,
            agreement_id: int,
            ip: Text,
            *,
            user_id: Optional[int] = MISSING,
            url: Optional[Text] = MISSING,
            origin_id: Optional[Text] = MISSING,
            originator_id: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Save the user consent

        Documentation: https://apidocs.bitrix24.com/api-reference/user-consent/user-consent-consent-add.html

        The method saves the user's consent.

        Args:
            agreement_id: Agreement identifier;

            ip: User's IP address;

            user_id: User identifier;

            url: URL of the page where consent was obtained;

            origin_id: Identifier of the source;

            originator_id: Identifier of the element in the source;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "AGREEMENT_ID": agreement_id,
            "IP": ip,
        }

        if user_id is not MISSING:
            params["USER_ID"] = user_id

        if url is not MISSING:
            params["URL"] = url

        if origin_id is not MISSING:
            params["ORIGIN_ID"] = origin_id

        if originator_id is not MISSING:
            params["ORIGINATOR_ID"] = originator_id

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params or None,
            timeout=timeout,
        )
