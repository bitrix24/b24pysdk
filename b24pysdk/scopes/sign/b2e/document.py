from typing import Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Document",
]


class Document(BaseEntity):
    """Methods for working with documents in e-Signature.

    Documentation: https://apidocs.bitrix24.com/api-reference/sign/index.html
    """

    @type_checker
    def get(
            self,
            uid: Text,
            *,
            language: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get document

        Documentation: https://apidocs.bitrix24.com/api-reference/sign/sign-b2e-document-get.html

        The method returns information about the document and signing participants.

        Args:
            uid: Unique identifier of the document;

            language: Language for localizing statuses in the response;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "uid": uid,
        }

        if language is not MISSING:
            params["language"] = language

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def send(
            self,
            fields: JSONDict,
            *,
            language: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Send document for signing

        Documentation: https://apidocs.bitrix24.com/api-reference/sign/sign-b2e-document-send.html

        The method sends a document for signing on behalf of the company.

        Args:
            fields: Parameters for sending the document for signing;

            language: Language for localizing statuses in the response;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "fields": fields,
        }

        if language is not MISSING:
            params["language"] = language

        return self._make_bitrix_api_request(
            api_wrapper=self.send,
            params=params,
            timeout=timeout,
        )
