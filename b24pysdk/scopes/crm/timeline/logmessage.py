from typing import Optional

from ....bitrix_api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from .._base_crm import BaseCRM

__all__ = [
    "Logmessage",
]


class Logmessage(BaseCRM):
    """These methods offer capabilities for working with the log message journal, where the log message journal is a special type of timeline record.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/logmessage/index.html
    """

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add log entry.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/logmessage/crm-timeline-logmessage-add.html

        This method adds a new log entry to the timeline.

        Args:
            fields: Object format:

                {
                    entityTypeId: "value",

                    entityId: "value",

                    title: "value",

                    text: "value",

                    iconCode: "value",
                };

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
        """Get information about the log entry.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/logmessage/crm-timeline-logmessage-get.html

        This method retrieves information about a timeline log entry.

        Args:
            bitrix_id: Integer identifier of the timeline entry;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._get(bitrix_id, timeout=timeout)

    @type_checker
    def list(
            self,
            entity_type_id: int,
            entity_id: id,
            *,
            order: Optional[JSONDict] = None,
            start: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of log entries.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/logmessage/crm-timeline-logmessage-list.html

        This method retrieves a list of timeline log entries.

        Args:
            entity_type_id: Identifier of the entity type for which to retrieve the list of log entries;

            entity_id: Identifier of the entity item for which to retrieve the list of log entries;

            order: Object format:

                {
                    field_1: value_1,

                    ...,
                }

                where

                - field_n is the name of the field by which the selection will be sorted

                - value_n is a string value equals to 'asc' (ascending sort) or 'desc' (descending sort);

            start: This parameter is used for pagination control;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "entityTypeId": entity_type_id,
            "entityId": entity_id,
        }

        if order is not None:
            params["order"] = order

        if start is not None:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
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
        """Delete log entry.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/logmessage/crm-timeline-logmessage-delete.html

        This method deletes a timeline log entry.

        Args:
            bitrix_id: Integer identifier of the timeline entry;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._delete(
            bitrix_id,
            timeout=timeout,
        )
