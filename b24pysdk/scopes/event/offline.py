from typing import Iterable, Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Offline",
]


class Offline(BaseEntity):
    """Methods for managing offline events in Bitrix24.

    Documentation: https://apidocs.bitrix24.com/api-reference/events/offline-events.html
    """

    @type_checker
    def get(
            self,
            *,
            filter: Optional[JSONDict] = MISSING,
            order: Optional[JSONDict] = MISSING,
            limit: Optional[int] = MISSING,
            clear: Optional[bool] = MISSING,
            process_id: Optional[Text] = MISSING,
            auth_connector: Optional[Text] = MISSING,
            error: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Retrieve a list of offline events with cleanup

        Documentation: https://apidocs.bitrix24.com/api-reference/events/event-offline-get.html

        The method returns the first offline events in the queue to the application according to the filter settings.

        Args:
            filter: Record filter;

            order: Record sorting;

            limit: Number of limits to select;

            clear: Values: 0|1 — whether to delete selected records. Default is 1;

            process_id: Process identifier;

            auth_connector: Source key;

            error: Values: 0|1 — whether to return erroneous records. Default is 0;

            timeout: Timeout in seconds.

        Return:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if filter is not MISSING:
            params["filter"] = filter

        if order is not MISSING:
            params["order"] = order

        if limit is not MISSING:
            params["limit"] = limit

        if clear is not MISSING:
            params["clear"] = int(clear)

        if process_id is not MISSING:
            params["process_id"] = process_id

        if auth_connector is not MISSING:
            params["auth_connector"] = auth_connector

        if error is not MISSING:
            params["error"] = int(error)

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            filter: Optional[JSONDict] = MISSING,
            order: Optional[JSONDict] = MISSING,
            start: Optional[int] = MISSING,
            auth_connector: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of offline events

        Documentation: https://apidocs.bitrix24.com/api-reference/events/event-offline-list.html

        A method for reading the current queue without making changes to its state.

        Args:
            filter: Record filter;

            order: Record sorting;

            auth_connector: Source key;

            timeout: Timeout in seconds.

        Return:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if filter is not MISSING:
            params["filter"] = filter

        if order is not MISSING:
            params["order"] = order

        if start is not MISSING:
            params["start"] = start

        if auth_connector is not MISSING:
            params["auth_connector"] = auth_connector

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def clear(
            self,
            process_id: Text,
            *,
            bitrix_id: Optional[Iterable[int]] = MISSING,
            message_id: Optional[Iterable[int]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Clear offline event queue

        Documentation: https://apidocs.bitrix24.com/api-reference/events/event-offline-clear.html

        The method clears the records in the offline event queue.

        Args:
            process_id: Identifier of the reserved event package;

            bitrix_id: Array of identifiers of records to be cleared;

            message_id: Array of values of the message field of records to be cleared;

            timeout: Timeout in seconds.

        Return:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "process_id": process_id,
        }

        if bitrix_id is not MISSING:
            if bitrix_id.__class__ is not list:
                bitrix_id = list(bitrix_id)

            params["id"] = bitrix_id

        if message_id is not MISSING:
            if message_id.__class__ is not list:
                message_id = list(message_id)

            params["message_id"] = message_id

        return self._make_bitrix_api_request(
            api_wrapper=self.clear,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def error(
            self,
            process_id: Text,
            *,
            message_id: Optional[Iterable[int]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Register offline event queue processing errors

        Documentation: https://apidocs.bitrix24.com/api-reference/events/event-offline-error.html

        The method retains a database records marked with an error when using offline events.

        Args:
            process_id: Identifier of the process that is handling the records;

            message_id: Array of values for the message field of the records to be marked as erroneous;

            timeout: Timeout in seconds.

        Return:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "process_id": process_id,
        }

        if message_id is not MISSING:
            if message_id.__class__ is not list:
                message_id = list(message_id)

            params["message_id"] = message_id

        return self._make_bitrix_api_request(
            api_wrapper=self.error,
            params=params,
            timeout=timeout,
        )
