from typing import Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Numerator",
]


class Numerator(BaseEntity):
    """Class handles numbering rules.

    Documentation: https://apidocs.bitrix24.com/api-reference/document-generator/numerators/index.html
    """

    @type_checker
    def add(
        self,
        fields: JSONDict,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add document generator numerator

        Documentation: https://apidocs.bitrix24.com/api-reference/document-generator/numerators/document-generator-numerator-add.html

        The method creates a document numerator.

        Args:
            fields: Document generator numerator parameters;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
        self,
        bitrix_id: int,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete the document generator numerator

        Documentation: https://apidocs.bitrix24.com/api-reference/document-generator/numerators/document-generator-numerator-delete.html

        The method removes a numerator by its identifier.

        Args:
            bitrix_id: Identifier of the numerator;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
        self,
        bitrix_id: int,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get numerator by ID

        Documentation: https://apidocs.bitrix24.com/api-reference/document-generator/numerators/document-generator-numerator-get.html

        The method returns the numerator data by its ID.

        Args:
            bitrix_id: The identifier of the numerator;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
        self,
        *,
        start: Optional[int] = MISSING,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of numerators

        Documentation: https://apidocs.bitrix24.com/api-reference/document-generator/numerators/document-generator-numerator-list.html

        The method returns a list of numerators for the document generator.

        Args:
            start: This parameter is used for managing pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {}

        if start is not MISSING:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
        self,
        bitrix_id: int,
        *,
        fields: Optional[JSONDict] = MISSING,
        name: Optional[Text] = MISSING,
        template: Optional[Text] = MISSING,
        settings: Optional[JSONDict] = MISSING,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update the numerator

        Documentation: https://apidocs.bitrix24.com/api-reference/document-generator/numerators/document-generator-numerator-update.html

        The method updates the numerator by its identifier.

        Args:
            bitrix_id: Identifier of the numerator;

            name: New name for the numerator;

            template: New template for the numerator;

            settings: New settings for the numerator;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        if fields is MISSING:
            fields = {}

            if name is not MISSING:
                fields["name"] = name

            if template is not MISSING:
                fields["template"] = template

            if settings is not MISSING:
                fields["settings"] = settings

        params: JSONDict = {
            "id": bitrix_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
