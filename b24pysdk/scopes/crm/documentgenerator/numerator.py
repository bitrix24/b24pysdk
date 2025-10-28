from typing import Optional

from ....bitrix_api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from .._base_crm import BaseCRM

__all__ = [
    "Numerator",
]


class Numerator(BaseCRM):
    """The methods provide capabilities for managing numberers.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/document-generator/numerator/index.html
    """

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add a new numerator.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/document-generator/numerator/crm-document-generator-numerator-add.html

        The method adds a new numerator.

        Args:
            fields: Object in the format:

                {
                    name: value,

                    template: value,

                    settings: value,
                };

            timeout: Timeout in seconds;

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._add(fields=fields, timeout=timeout)

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get information about the numerator by ID.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/document-generator/numerator/crm-document-generator-numerator-get.html

        The method returns information about the numerator by its identifier.

        Args:
            bitrix_id: Identifier of the numerator;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._get(bitrix_id=bitrix_id, timeout=timeout)

    @type_checker
    def list(
            self,
            *,
            start: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of numerators.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/document-generator/numerator/crm-document-generator-numerator-list.html

        The method returns a list of numerators.

        Args:
            start: The parameter is used to manage pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._list(start=start, timeout=timeout)

    @type_checker
    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update existing numbering.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/document-generator/numerator/crm-document-generator-numerator-update.html

        The method updates an existing numbering with new values.

        Args:
            bitrix_id: Identifier of the numbering;

            fields: Object in the format:

                {
                    name: value,

                    template: value,

                    settings: value,
                };

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._update(
            bitrix_id=bitrix_id,
            fields=fields,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete numerator.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/document-generator/numerator/crm-document-generator-numerator-delete.html

        The method removes a numerator.

        Args:
            bitrix_id: Identifier of the numerator;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._delete(bitrix_id=bitrix_id, timeout=timeout)
