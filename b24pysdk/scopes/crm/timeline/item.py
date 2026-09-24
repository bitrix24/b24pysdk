from typing import Optional

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from .._base_crm import BaseCRM

__all__ = [
    "Item",
]


class Item(BaseCRM):
    """Class for managing pinned records in the timeline.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/actions/index.html
    """

    @type_checker
    def pin(
            self,
            bitrix_id: int,
            owner_type_id: int,
            owner_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[Optional[bool]]:
        """Pin a timeline entry

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/actions/crm-timeline-item-pin.html

        The method pins an entry in the timeline.

        Args:
            bitrix_id: Identifier of the timeline item;

            owner_type_id: Identifier of the CRM object type to which the item is linked;

            owner_id: Identifier of the CRM element to which the item is linked;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIValuesRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
            "ownerTypeId": owner_type_id,
            "ownerId": owner_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.pin,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unpin(
            self,
            bitrix_id: int,
            owner_type_id: int,
            owner_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[Optional[bool]]:
        """Unpin a timeline entry

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/actions/crm-timeline-item-unpin.html

        The method unpins a timeline entry.

        Args:
            bitrix_id: Identifier of the timeline item;

            owner_type_id: Identifier of the CRM object type to which the item is linked;

            owner_id: Identifier of the CRM element to which the item is linked;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIValuesRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
            "ownerTypeId": owner_type_id,
            "ownerId": owner_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.unpin,
            params=params,
            timeout=timeout,
        )
