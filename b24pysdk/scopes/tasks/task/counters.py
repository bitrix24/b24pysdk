from typing import Annotated, Literal, Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Counters",
]


class Counters(BaseEntity):
    """Class for retrieving user counters.

    Documentation: https://apidocs.bitrix24.com/api-reference/tasks/index.html
    """

    @type_checker
    def get(
            self,
            *,
            user_id: Optional[int] = MISSING,
            group_id: Optional[int] = MISSING,
            type: Optional[Annotated[Text, Literal[
                "view_all",
                "view_role_responsible",
                "view_role_accomplice",
                "view_role_auditor",
                "view_role_originator",
            ]]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get user counters

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/tasks-task-counters-get.html

        The method retrieves task counter values for the specified user.

        Args:
            user_id: The identifier of the user for whom to retrieve counters;

            group_id: The identifier of the group for which to retrieve task counters;

            type: The role for which to retrieve counters;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if user_id is not MISSING:
            params["userId"] = user_id

        if group_id is not MISSING:
            params["groupId"] = group_id

        if type is not MISSING:
            params["type"] = type

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )
