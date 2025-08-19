from typing import TYPE_CHECKING

from .....bitrix_api.classes import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...base_crm import BaseCRM

if TYPE_CHECKING:
    from .layout import Layout


class Blocks(BaseCRM):
    """These methods offer capabilities for working with additional content blocks in an activity.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/layout-blocks/index.html
    """

    def __init__(self, layout: "Layout"):
        super().__init__(layout._scope)
        self._path = self._get_path(layout)

    @type_checker
    def get(
            self,
            *,
            entity_type_id: int,
            entity_id: int,
            activity_id: int,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a set of additional content blocks in the activity.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/layout-blocks/crm-activity-layout-blocks-get.html

        This method allows a REST application to retrieve a set of additional content blocks in the activity that it has set.
        The REST application can only obtain the set of additional content blocks that it has established.

        Args:
            entity_type_id: Identifier of the CRM object type to which the activity is linked;

            entity_id: Identifier of the CRM object to which the activity is linked;

            activity_id: Identifier of the activity;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "entityTypeId": entity_type_id,
            "entityId": entity_id,
            "activityId": activity_id,
        }

        return self._make_bitrix_api_request(
            api_method=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set(
            self,
            *,
            entity_type_id: int,
            entity_id: int,
            activity_id: int,
            layout: JSONDict,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Set a set of additional content blocks in the activity.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/layout-blocks/crm-activity-layout-blocks-set.html

        This method allows REST applications to set a set of additional content blocks in an activity.

        Args:
            entity_type_id: Identifier of the CRM object type to which the activity is linked;

            entity_id: Identifier of the CRM object to which the activity is linked;

            activity_id: Identifier of the activity;

            layout: Object describing the set of additional content blocks;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "entityTypeId": entity_type_id,
            "entityId": entity_id,
            "activityId": activity_id,
            "layout": layout,
        }

        return self._make_bitrix_api_request(
            api_method=self.set,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            *,
            entity_type_id: int,
            entity_id: int,
            activity_id: int,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete a set of additional content blocks in CRM activity.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/layout-blocks/crm-activity-layout-blocks-delete.html

        The method allows a REST application to delete a set of additional content blocks that it has installed for an activity.
        A REST application can only delete the set of additional content blocks that it has installed.

        Args:
            entity_type_id: Identifier of the CRM object type to which the activity is linked;

            entity_id: Identifier of the CRM object to which the activity is linked;

            activity_id: Identifier of the activity;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "entityTypeId": entity_type_id,
            "entityId": entity_id,
            "activityId": activity_id,
        }

        return self._make_bitrix_api_request(
            api_method=self.delete,
            params=params,
            timeout=timeout,
        )
