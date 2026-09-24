from typing import Annotated, Iterable, List, Literal, Text, Union

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest, BitrixAPIValuesRequest
from ...schemas.sonet_group.user import SonetGroupMember, SonetGroupMembersData, SonetGroupUserGroup, SonetGroupUserGroupsData
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._adapters import BitrixSchemasAdapter
from .._base_entity import BaseEntity

__all__ = [
    "User",
]


class User(BaseEntity):
    """Class for managing users in groups.

    Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/index.html
    """

    @type_checker
    def add(
            self,
            group_id: int,
            user_id: Union[int, Iterable[int]],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[List[Text]]:
        """Add users to group

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/members/sonet-group-user-add.html

        The method adds users to a workgroup or project without an invitation and confirmation.

        Args:
            group_id: Identifier of the workgroup or project;

            user_id: User identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if user_id.__class__ is not list and not isinstance(user_id, int):
            user_id = list(user_id)

        params: JSONDict = {
            "GROUP_ID": group_id,
            "USER_ID": user_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            group_id: int,
            user_id: Union[int, Iterable[int]],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[List[Text]]:
        """Remove user from group

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/members/sonet-group-user-delete.html

        The method removes participants from a workgroup or project.

        Args:
            group_id: Identifier of the workgroup or project;

            user_id: Identifier of the participant;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if user_id.__class__ is not list and not isinstance(user_id, int):
            user_id = list(user_id)

        params: JSONDict = {
            "GROUP_ID": group_id,
            "USER_ID": user_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            group_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIValuesRequest[SonetGroupMembersData, SonetGroupMember]:
        """Get the list of group participants

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/members/sonet-group-user-get.html

        The method returns a list of active participants in a workgroup or project.

        Args:
            group_id: Identifier of the workgroup or project;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "ID": group_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValuesRequest,
            result_adapter=BitrixSchemasAdapter(SonetGroupMember),
        )

    @type_checker
    def groups(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIValuesRequest[SonetGroupUserGroupsData, SonetGroupUserGroup]:
        """Get the list of groups for the current user

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/sonet-group-user-groups.html

        The method returns the groups and projects that the current user is a member of.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.groups,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValuesRequest,
            result_adapter=BitrixSchemasAdapter(SonetGroupUserGroup),
        )

    @type_checker
    def invite(
            self,
            group_id: int,
            user_id: Union[int, Iterable[int]],
            *,
            message: Text = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[List[Text]]:
        """Invite users to group

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/members/sonet-group-user-invite.html

        The method sends invitations to users in a workgroup or project.

        Args:
            group_id: Identifier of the workgroup or project;

            user_id: User identifier;

            message: Invitation text;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if user_id.__class__ is not list and not isinstance(user_id, int):
            user_id = list(user_id)

        params: JSONDict = {
            "GROUP_ID": group_id,
            "USER_ID": user_id,
        }

        if message is not MISSING:
            params["MESSAGE"] = message

        return self._make_bitrix_api_request(
            api_wrapper=self.invite,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def request(
            self,
            group_id: int,
            *,
            message: Text = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Send a request to join the group

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/members/sonet-group-user-request.html

        The method sends a request from the current user to join a workgroup or project.

        Args:
            group_id: Identifier of the workgroup or project;

            message: Text of the request to join;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "GROUP_ID": group_id,
        }

        if message is not MISSING:
            params["MESSAGE"] = message

        return self._make_bitrix_api_request(
            api_wrapper=self.request,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            group_id: int,
            user_id: Union[int, Iterable[int]],
            role: Annotated[Text, Literal["E", "K"]],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[List[Text]]:
        """Change role of group participants

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/members/sonet-group-user-update.html

        The method changes the role of participants in a workgroup or project.

        Args:
            group_id: Identifier of the workgroup or project;

            user_id: User identifier;

            role: Code of the new participant role;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if user_id.__class__ is not list and not isinstance(user_id, int):
            user_id = list(user_id)

        params: JSONDict = {
            "GROUP_ID": group_id,
            "USER_ID": user_id,
            "ROLE": role,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
