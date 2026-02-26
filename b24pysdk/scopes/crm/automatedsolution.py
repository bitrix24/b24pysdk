from typing import Optional

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from ._base_crm import BaseCRM

__all__ = [
    "Automatedsolution",
]


class Automatedsolution(BaseCRM):
    """The class provide methods for managing digital workspaces.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/automated-solution/index.html
    """

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get fields of the digital workplace.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/automated-solution/crm-automated-solution-fields.html

        This method returns information about the fields of the digital workplace settings.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._fields(timeout=timeout)

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create digital workspace.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/automated-solution/crm-automated-solution-add.html

        This method will create a new digital workspace.

        Args:
            fields: Field values for creating a digital workspace in the form of a structure:

                {
                    "title": "value",

                    "typeIds": []
                }

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._add(fields, timeout=timeout)

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get digital workplace data by ID.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/automated-solution/crm-automated-solution-get.html

        This method returns information about the digital workplace with the identifier.

        Args:
            bitrix_id: Identifier of the digital workplace;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._get(bitrix_id=bitrix_id, timeout=timeout)

    @type_checker
    def list(
            self,
            *,
            filter: Optional[JSONDict] = None,
            order: Optional[JSONDict] = None,
            start: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of digital workspaces.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/automated-solution/crm-automated-solution-get.html

        The method will return an array of digital workspace settings.

        Args:
            filter: Object format:

                {
                    "field_1": "value_1",

                    ...,

                    "field_N": "value_N"
                }

            order: List for sorting;

            start: This parameter is used for pagination control;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._list(
            filter=filter,
            order=order,
            start=start,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update digital workplace.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/automated-solution/crm-automated-solution-update.html

        This method updates the existing settings of the digital workplace with the identifier.

        Args:
            bitrix_id: Identifier of the digital workplace;

            fields: Object format:

                {
                    "field_1": "value_1",

                    ...,

                    "field_N": "value_N"
                }

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._update(
            bitrix_id,
            fields,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete digital workplace.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/automated-solution/crm-automated-solution-delete.html

        This method deletes an existing digital workplace with the identifier.

        Args:
            bitrix_id: Identifier of the digital workplace.

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._delete(bitrix_id=bitrix_id, timeout=timeout)
