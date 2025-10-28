from ....bitrix_api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from .._base_crm import BaseCRM

__all__ = [
    "Configurable",
]


class Configurable(BaseCRM):
    """The methods provide capabilities for working with configurable activities in timeline.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/configurable/index.html
    """

    @type_checker
    def add(
            self,
            *,
            owner_type_id: int,
            owner_id: int,
            fields: JSONDict,
            layout: JSONDict,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add configurable activity.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/configurable/crm-activity-configurable-add.html

        The method adds a configurable activity to the timeline.

        Args:
            owner_type_id: Identifier of the CRM entity type where the activity is created;

            owner_id: Identifier of the CRM element where the activity is created;

            fields: Object format:

                {
                    "typeId": 'value',

                    "completed": 'value',

                    "deadline": 'value',

                    "pingOffsets": 'value',

                    "isIncomingChannel": 'value',

                    "responsibleId": 'value',

                    "badgeCode": 'value',

                    "originatorId": 'value',

                    "originId": 'value',
                };

            layout: Associative array of a special structure describing the appearance of the activity in the timeline;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "ownerTypeId": owner_type_id,
            "ownerId": owner_id,
            "fields": fields,
            "layout": layout,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
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
        """Get configurable activity by ID.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/configurable/crm-activity-configurable-get.html

        The method returns information about a configurable activity.

        Args:
            bitrix_id: Identifier od the activity;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._get(bitrix_id, timeout=timeout)

    @type_checker
    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update configurable activity.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/configurable/crm-activity-configurable-update.html

        The method makes changes to a configurable activity.

        Args:
            bitrix_id: Identifier of the activity;

            fields: Object format:

                {
                    "typeId": 'value',

                    "completed": 'value',

                    "deadline": 'value',

                    "pingOffsets": 'value',

                    "isIncomingChannel": 'value',

                    "responsibleId": 'value',

                    "badgeCode": 'value',

                    "originatorId": 'value',

                    "originId": 'value',
                };

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._update(
            bitrix_id,
            fields,
            timeout=timeout,
        )
