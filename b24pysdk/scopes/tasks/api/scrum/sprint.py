from typing import Iterable, Optional, Text

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "Sprint",
]


class Sprint(BaseEntity):
    """Class for managing sprints in Scrum.

    Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/scrum/sprint/index.html
    """

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add sprint in Scrum

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/scrum/sprint/tasks-api-scrum-sprint-add.html

        The method adds a sprint to Scrum.

        Args:
            fields: Object containing sprint data;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def complete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Complete the active sprint of the selected Scrum

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/scrum/sprint/tasks-api-scrum-sprint-complete.html

        The method completes the active sprint of the selected Scrum.

        Args:
            bitrix_id: Identifier of the group with the active sprint;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.complete,
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
        """Delete sprint

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/scrum/sprint/tasks-api-scrum-sprint-delete.html

        The method deletes a sprint.

        Args:
            bitrix_id: Identifier of the sprint;

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
    def get(
            self,
            sprint_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get sprint fields by ID

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/scrum/sprint/tasks-api-scrum-sprint-get.html

        The method returns the values of the sprint fields by its identifier.

        Args:
            sprint_id: Identifier of the sprint;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": sprint_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of available fields for the sprint

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/scrum/sprint/tasks-api-scrum-sprint-get-fields.html

        The method returns the available fields for the sprint.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.get_fields,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            order: Optional[JSONDict] = MISSING,
            filter: Optional[JSONDict] = MISSING,
            select: Optional[Iterable[Text]] = MISSING,
            start: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of sprints

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/scrum/sprint/tasks-api-scrum-sprint-list.html

        The method returns a list of sprints.

        Args:
            order: An object for sorting the selected records, where the key is the field and the value is asc or desc;

            filter: Object for filtering the result;

            select: Array of fields of records that will be returned by the method;

            start: The page number of the output;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if order is not MISSING:
            params["order"] = order

        if filter is not MISSING:
            params["filter"] = filter

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        if start is not MISSING:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def start(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Start sprint

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/scrum/sprint/tasks-api-scrum-sprint-start.html

        The method initiates a sprint.

        Args:
            bitrix_id: Identifier of the sprint;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.start,
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
        """Update sprint

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/scrum/sprint/tasks-api-scrum-sprint-update.html

        The method updates a sprint.

        Args:
            bitrix_id: Identifier of the sprint;

            fields: Object containing sprint data

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
