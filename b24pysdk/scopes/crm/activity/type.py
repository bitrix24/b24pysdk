from typing import Text

from ....bitrix_api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from .._base_crm import BaseCRM

__all__ = [
    "Type",
]


class Type(BaseCRM):
    """The methods provide capabilities for working with custom activity types.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/types/index.html
    """

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add custom CRM activity type.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/types/crm-activity-type-add.html

        The method register a custom activity type by specifying its name and icon.

        Args:
            fields: Object format:

                {
                    "TYPE_ID": 'value',

                    "NAME": 'value',

                    "ICON_FILE": 'value',

                    "IS_CONFIGURABLE_TYPE": 'value',
                };

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._add(fields, timeout=timeout)

    @type_checker
    def list(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of custom activity types.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/types/crm-activity-type-list.html

        The method retrieves a list of custom activity types registered by the application.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._list(timeout=timeout)

    @type_checker
    def delete(
            self,
            type_id: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete custom activity type.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/types/crm-activity-type-delete.html

        The method removes a custom activity type.

        Args:
            type_id: String value of the activity type;

            timeout: Timeout in seconds.

        Returns:
            BitrixAPIRequest
        """

        params = {
            "TYPE_ID": type_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )
