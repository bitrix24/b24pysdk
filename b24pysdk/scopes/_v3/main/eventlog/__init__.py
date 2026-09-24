from functools import cached_property
from typing import Iterable, Optional, Text

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity
from ..._field import Field

__all__ = [
    "Eventlog",
]


class Eventlog(BaseEntity):
    """Class for retrieving log records of user actions.

    Documentation: https://apidocs.bitrix24.com/api-reference/event-log/index.html
    """

    @cached_property
    def field(self) -> Field:
        """"""
        return Field(self)

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            select: Optional[Iterable[Text]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get event log entry

        Documentation: https://apidocs.bitrix24.com/api-reference/event-log/main-eventlog-get.html

        The method returns an event log entry by its identifier.

        Args:
            bitrix_id: identifier of the log entry;

            select: List of fields to return in the response;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
        }

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)
            params["select"] = select

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            select: Optional[Iterable[Text]] = MISSING,
            filter: Optional[Iterable] = MISSING,
            order: Optional[JSONDict] = MISSING,
            pagination: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of event log entries

        Documentation: https://apidocs.bitrix24.com/api-reference/event-log/main-eventlog-list.html

        The method returns a list of event log entries based on specified conditions.

        Args:
            select: List of fields to return in the response;

            filter: Conditions for filtering entries;

            order: Sorting direction;

            pagination: Pagination parameters;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)
            params["select"] = select

        if filter is not MISSING:
            if filter.__class__ is not list:
                filter = list(filter)
            params["filter"] = filter

        if order is not MISSING:
            params["order"] = order

        if pagination is not MISSING:
            params["pagination"] = pagination

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def tail(
            self,
            *,
            select: Optional[Iterable[Text]] = MISSING,
            filter: Optional[Iterable] = MISSING,
            cursor: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get new log entries

        Documentation: https://apidocs.bitrix24.com/api-reference/event-log/main-eventlog-tail.html

        The method returns new log entries that appeared after the specified cursor reference point, considering the filter.

        Args:
            select: List of fields to return in the response;

            filter: Conditions for filtering records;

            cursor: Reference point for retrieving new records;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)
            params["select"] = select

        if filter is not MISSING:
            if filter.__class__ is not list:
                filter = list(filter)
            params["filter"] = filter

        if cursor is not MISSING:
            params["cursor"] = cursor

        return self._make_bitrix_api_request(
            api_wrapper=self.tail,
            params=params,
            timeout=timeout,
        )
