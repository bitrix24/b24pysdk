from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "Document",
]


class Document(BaseEntity):
    """Class for retrieving data of a signed document linked to HCM Link.

    Documentation: https://apidocs.bitrix24.com/api-reference/sign/index.html
    """

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Retrieve signed HCM link document

        Documentation: https://apidocs.bitrix24.com/api-reference/sign/sign-b2e-hcmlink-document-get.html

        The method returns data of a signed e-Signature for HR document linked to HCM Link.

        Args:
            bitrix_id: Signing participant identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )
