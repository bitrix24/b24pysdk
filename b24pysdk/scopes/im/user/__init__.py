from functools import cached_property
from typing import Optional, Text, Union

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.converters import bool_to_bitrix
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity
from .list import List
from .status import Status

__all__ = [
    "User",
]


class User(BaseEntity):
    """Class for retrieving user data.

    Documentation: https://apidocs.bitrix24.com/api-reference/chats/users/index.html
    """

    @cached_property
    def list(self) -> List:
        """"""
        return List(self)

    @cached_property
    def status(self) -> Status:
        """"""
        return Status(self)

    @type_checker
    def get(
            self,
            *,
            bitrix_id: Optional[Union[int, Text]] = MISSING,
            avatar_hr: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """Get user data

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/users/im-user-get.html

        The retrieves data about the current user or a user by ID.

        Args:
            bitrix_id: User identifier;

            avatar_hr: Frog for requesting avatar;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if bitrix_id is not MISSING:
            params["ID"] = bitrix_id

        if avatar_hr is not MISSING:
            params["AVATAR_HR"] = bool_to_bitrix(avatar_hr, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params or None,
            timeout=timeout,
        )
