from typing import Optional

from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ..._base_crm import BaseCRM

__all__ = [
    "Blocks",
]


class Blocks(BaseCRM):
    """Class for managing additional content blocks for the timeline.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/layout-blocks/index.html
    """

    @type_checker
    def get(
            self,
            entity_type_id: int,
            entity_id: int,
            timeline_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """Retrieve a set of additional content blocks for the timeline record

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/layout-blocks/crm-timeline-layout-blocks-get.html

        The method retrieves a set of additional content blocks for a timeline record.

        Args:
            entity_type_id: Identifier of the CRM object type associated with the timeline record;

            entity_id: Identifier of the CRM object associated with the timeline record;

            timeline_id: Identifier of the timeline record;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIValuesRequest
        """

        params: JSONDict = {
            "entityTypeId": entity_type_id,
            "entityId": entity_id,
            "timelineId": timeline_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set(
            self,
            entity_type_id: int,
            entity_id: int,
            timeline_id: int,
            layout: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Set a set of additional content blocks in the CRM timeline record

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/layout-blocks/crm-timeline-layout-blocks-set.html

        The method sets a set of additional content blocks for a timeline record.

        Args:
            entity_type_id: Identifier of the CRM object to which the timeline record is linked;

            entity_id: Identifier of the CRM object to which the timeline record is linked;

            timeline_id: Identifier of the timeline record;

            layout: Object describing the set of additional content blocks;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIValuesRequest
        """

        params: JSONDict = {
            "entityTypeId": entity_type_id,
            "entityId": entity_id,
            "timelineId": timeline_id,
            "layout": layout,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.set,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            entity_type_id: int,
            entity_id: int,
            timeline_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[Optional[bool]]:
        """Delete a set of additional content blocks for the timeline record

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/layout-blocks/crm-timeline-layout-blocks-delete.html

        The method removes a set of additional content blocks for a timeline record.

        Args:
            entity_type_id: Identifier of the CRM object to which the timeline record is linked;

            entity_id: Identifier of the CRM object to which the timeline record is linked;

            timeline_id: Identifier of the timeline record;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIValuesRequest
        """

        params: JSONDict = {
            "entityTypeId": entity_type_id,
            "entityId": entity_id,
            "timelineId": timeline_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

