from typing import TYPE_CHECKING, Text, Union

from ....bitrix_api.classes import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..base_crm import BaseCRM

if TYPE_CHECKING:
    from .activity import Activity


class Badge(BaseCRM):
    """The methods provide capabilities for managing activity badges.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/configurable/badges/index.html
    """

    def __init__(self, activity: "Activity"):
        super().__init__(scope=activity._scope)
        self._path = self._get_path(activity)

    @type_checker
    def add(
            self,
            code: Text,
            title: Union[Text, JSONDict],
            value: Union[Text, JSONDict],
            type: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add badge

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/configurable/badges/crm-activity-badge-add.html

        The method adds a new badge for a configurable activity.

        Args:
            code: Badge code;

            title: badge title;

            value: badge value;

            type: badge type;

            timeout: Timeout in seconds.

        Returns:
            BitrixAPIRequest
        """

        params = {
            "code": code,
            "title": title,
            "value": value,
            "type": type,
        }

        return self._make_bitrix_api_request(
            api_method=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            code: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get badge information by code.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/configurable/badges/crm-activity-badge-get.html

        The method will return an array containing badge fields.

        Args:
            code: Badge code;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "code": code,
        }

        return self._make_bitrix_api_request(
            api_method=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of badges.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/configurable/badges/crm-activity-badge-list.html

        the method retrieves a list of available badges.

        Args:
            timeout: Timeout in seconds.

        Returns:
              Instance of BitrixAPIRequest
        """

        return self._list(timeout=timeout)

    @type_checker
    def delete(
            self,
            code: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete badge by code.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/configurable/badges/crm-activity-badge-delete.html

        The method removes a badge.

        Args:
            code: Badge code;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "code": code,
        }

        return self._make_bitrix_api_request(
            api_method=self.delete,
            params=params,
            timeout=timeout,
        )
