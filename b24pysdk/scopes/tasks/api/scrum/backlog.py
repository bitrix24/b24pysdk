from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "Backlog",
]


class Backlog(BaseEntity):
    """Class for managing the backlog - a list of all the team's tasks.

    Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/scrum/backlog/index.html
    """

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add backlog in Scrum

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/scrum/backlog/tasks-api-scrum-backlog-add.html

        The method adds a backlog in Scrum.

        Args:
            fields: An object containing records about the group and user;

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
    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete backlog

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/scrum/backlog/tasks-api-scrum-backlog-delete.html

        The method removes the backlog.

        Args:
            bitrix_id: The ID of the backlog;

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
    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update backlog

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/scrum/backlog/tasks-api-scrum-backlog-update.html

        The method updates the backlog.

        Args:
            bitrix_id: Backlog identifier;

            fields: An object containing records about the group and user;

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
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get backlog fields by Scrum ID

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/scrum/backlog/tasks-api-scrum-backlog-get.html

        The method returns the values of backlog fields by Scrum id.

        Args:
            bitrix_id: Identifier of the group;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
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
        """Get a list of available backlog fields

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/scrum/backlog/tasks-api-scrum-backlog-get-fields.html

        The method returns the available backlog fields.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.get_fields,
            timeout=timeout,
        )
