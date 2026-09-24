from typing import Optional

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.converters import bool_to_bitrix
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Timeline",
]


class Timeline(BaseEntity):
    """A set of methods for working with timeline records.

    Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/timeline/index.html
    """

    @type_checker
    def add(
            self,
            type_id: int,
            item_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add a new timeline entry

        Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/timeline/rpa-timeline-add.html

        This method creates a new timeline entry for the itemId of the typeId process.

        Args:
            type_id: Identifier of the process;

            item_id: Identifier of the item;

            fields: Object containing the fields of the entry;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "typeId": type_id,
            "itemId": item_id,
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
        """Delete timeline record

        Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/timeline/rpa-timeline-delete.html

        This method deletes a timeline record with the identifier id.

        Args:
            bitrix_id: Identifier of the record;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
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
    def list_for_item(
            self,
            type_id: int,
            item_id: int,
            *,
            start: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list timeline records list for the element

        Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/timeline/rpa-timeline-list-for-item.html

        This method retrieves a list of timeline records for the itemId of the typeId process.

        Args:
            type_id: Identifier of the process;

            item_id: Identifier of the element;

            start: This parameter is used for pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "typeId": type_id,
            "itemId": item_id,
        }

        if start is not MISSING:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.list_for_item,
            params=params,
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
        """Update timeline

        Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/timeline/rpa-timeline-update.html

        This method updates the timeline entry with the identifier id.

        Args:
            bitrix_id: Identifier of the entry;

            fields: Object containing the fields of the entry;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update_is_fixed(
            self,
            bitrix_id: int,
            is_fixed: bool,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update the attachment flag

        Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/timeline/rpa-timeline-update-is-fixed.html

        This method updates the attachment flag of a record.

        Args:
            bitrix_id: Identifier of the entry;

            is_fixed: Attachment flag of the record;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
            "isFixed": bool_to_bitrix(is_fixed, is_required=True),
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update_is_fixed,
            params=params,
            timeout=timeout,
        )
