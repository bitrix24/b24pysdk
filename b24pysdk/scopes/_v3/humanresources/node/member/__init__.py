from functools import cached_property
from typing import Iterable, Optional, Text

from ......_constants import MISSING
from ......api.requests import BitrixAPIRequest
from ......utils.functional import type_checker
from ......utils.types import JSONDict, Timeout
from ....._base_entity import BaseEntity
from ...._field import Field

__all__ = [
    "Member",
]


class Member(BaseEntity):
    """Class for managing departament or team memers.

    Documentation: https://apidocs.bitrix24.com/api-reference/departments/node-member/index.html
    """

    @cached_property
    def field(self) -> Field:
        """"""
        return Field(self)

    @type_checker
    def add(
            self,
            node_id: int,
            user_ids: Iterable[int],
            role: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """Add participants

        Documentation: https://apidocs.bitrix24.com/api-reference/departments/node-member/humanresources-node-member-add.html

        THe method adds users to a departament or team.

        Args:
            node_id: Identifier of the department or team;

            user_ids: An array of user identifiers to be added to the department or team;

            role: The role to be assigned to all users;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if user_ids.__class__ is not list:
            user_ids = list(user_ids)

        params: JSONDict = {
            "nodeId": node_id,
            "userIds": user_ids,
            "role": role,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def move(
            self,
            node_id: int,
            user_ids: Iterable[int],
            *,
            role: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """Move participants to the department

        Documentation: https://apidocs.bitrix24.com/api-reference/departments/node-member/humanresources-node-member-move.html

        The method transfers users to the specified department.

        Args:
            node_id: Identifier of the target department or team;

            user_ids: An array of user identifiers to be transferred;

            role: The role to be assigned to the transferred participants;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if user_ids.__class__ is not list:
            user_ids = list(user_ids)

        params: JSONDict = {
            "nodeId": node_id,
            "userIds": user_ids,
        }

        if role is not MISSING:
            params["role"] = role

        return self._make_bitrix_api_request(
            api_wrapper=self.move,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def remove(
            self,
            node_id: int,
            user_ids: Iterable[int],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """Remove participants from the department

        Documentation: https://apidocs.bitrix24.com/api-reference/departments/node-member/humanresources-node-member-remove.html

        The method removes users from the specified department or team.

        Args:
            node_id: Identifier of the department or team;

            user_ids: An array of user identifiers to be removed;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if user_ids.__class__ is not list:
            user_ids = list(user_ids)

        params: JSONDict = {
            "nodeId": node_id,
            "userIds": user_ids,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.remove,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set(
            self,
            node_id: int,
            user_ids: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """Update the composition of participants

        Documentation: https://apidocs.bitrix24.com/api-reference/departments/node-member/humanresources-node-member-set.html

        The method updates the composition of participants in a department or team by roles.

        Args:
            node_id: Identifier of the department or team;

            user_ids: An object containing lists of user identifiers to be updated;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "nodeId": node_id,
            "userIds": user_ids,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.set,
            params=params,
            timeout=timeout,
        )
