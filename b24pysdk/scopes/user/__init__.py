from functools import cached_property
from typing import Dict, Iterable, Literal, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest, BitrixAPIValueRequest, BitrixAPIValuesRequest
from ...objects.user import User as UserObject
from ...utils.functional import type_checker
from ...utils.types import JSONDict, JSONList, Timeout
from .._adapters import BitrixObjectAdapter, BitrixObjectsAdapter
from .._base_scope import BaseScope
from .option import Option
from .userfield import Userfield

__all__ = [
    "User",
]


class User(BaseScope):
    """Class for working with users and their profiles.

    Documentation: https://apidocs.bitrix24.com/api-reference/user/index.html
    """

    @cached_property
    def option(self) -> Option:
        """"""
        return Option(self)

    @cached_property
    def userfield(self) -> Userfield:
        """"""
        return Userfield(self)

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[Dict[Text, Text]]:
        """Get user fields

        Documentation: https://apidocs.bitrix24.com/api-reference/user/user-fields.html

        The method retrieves the list of user field names.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.fields,
            timeout=timeout,
        )

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIValueRequest[int, UserObject]:
        """Invite a user

        Documentation: https://apidocs.bitrix24.com/api-reference/user/user-add.html

        The method invites a user.

        Args:
            fields: Fields for inviting a user;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=fields,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValueRequest,
            result_adapter=BitrixObjectAdapter("user", client=self._client),
        )

    @type_checker
    def get(
            self,
            *,
            sort: Text = MISSING,
            order: Text = MISSING,
            filter: JSONDict = MISSING,
            select: Iterable[Text] = MISSING,
            image_resize: Literal["small", "medium", "large"] = MISSING,
            admin_mode: bool = MISSING,
            start: int = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIValuesRequest[JSONList, UserObject]:
        """Get a list of users by filter

        Documentation: https://apidocs.bitrix24.com/api-reference/user/user-get.html

        The method retrieves a filtered list of users.

        Args:
            sort: Sorting criteria;

            order: Sorting direction;

            filter: Filter for selecting users;

            select: List of fields to select;

            image_resize: The size of the photo copy in the PERSONAL_PHOTO field;

            admin_mode: Parameter used to obtain data about any user;

            start: The parameter is used to control pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if sort is not MISSING:
            params["sort"] = sort

        if order is not MISSING:
            params["order"] = order

        if filter is not MISSING:
            params["filter"] = filter

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        if image_resize is not MISSING:
            params["IMAGE_RESIZE"] = image_resize

        if admin_mode is not MISSING:
            params["ADMIN_MODE"] = int(admin_mode)

        if start is not MISSING:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValuesRequest,
            result_adapter=BitrixObjectsAdapter(
                object_key="user",
                client=self._client,
                select=params.get("select"),
            ),
        )

    @type_checker
    def update(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Update user

        Documentation: https://apidocs.bitrix24.com/api-reference/user/user-update.html

        The method updates user data.

        Args:
            fields: Fields to update;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=fields,
            timeout=timeout,
        )

    @type_checker
    def search(
            self,
            *,
            filter: JSONDict = MISSING,
            select: Iterable[Text] = MISSING,
            sort: Text = MISSING,
            order: Text = MISSING,
            admin_mode: bool = MISSING,
            start: int = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIValuesRequest[JSONList, UserObject]:
        """Get a list of users with personal data

        Documentation: https://apidocs.bitrix24.com/api-reference/user/user-search.html

        The method retrieves a list of users with accelerated search based on personal data.

        Args:
            filter: The array of fields for searching;

            select: An array with the names of the fields to return in the response;

            sort: The field by which the results are sorted;

            order: Sorting direction;

            admin_mode: Parameter used to obtain data about any users;

            start: The parameter is used to manage pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if filter is not MISSING:
            params["filter"] = filter

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        if sort is not MISSING:
            params["sort"] = sort

        if order is not MISSING:
            params["order"] = order

        if admin_mode is not MISSING:
            params["ADMIN_MODE"] = int(admin_mode)

        if start is not MISSING:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.search,
            params=params,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValuesRequest,
            result_adapter=BitrixObjectsAdapter(
                object_key="user",
                client=self._client,
                select=params.get("select"),
            ),
        )

    @type_checker
    def current(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIValueRequest[JSONDict, UserObject]:
        """Get information about the current user

        Documentation: https://apidocs.bitrix24.com/api-reference/user/user-current.html

        The method retrieves information about the current user.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.current,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValueRequest,
            result_adapter=BitrixObjectAdapter("user", client=self._client),
        )

    @type_checker
    def admin(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Determine access permissions for application settings

        Documentation: https://apidocs.bitrix24.com/api-reference/common/users/user-admin.html

        The method determines whether the current user has the permissions to manage application settings.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.admin,
            timeout=timeout,
        )

    @type_checker
    def access(
            self,
            access: Iterable[Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Determine the permissions set

        Documentation: https://apidocs.bitrix24.com/api-reference/common/users/user-access.html

        The method checks if the current user has at least one of the permissions specified in the ACCESS parameter.

        Args:
            access: List of the access codes to check;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if access.__class__ is not list:
            access = list(access)

        params: JSONDict = {
            "ACCESS": access,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.access,
            params=params,
            timeout=timeout,
        )
