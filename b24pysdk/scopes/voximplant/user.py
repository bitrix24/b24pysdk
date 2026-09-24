from typing import Iterable, Union

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "User",
]


class User(BaseEntity):
    """Class for managing users' SIP settings.

    Documentation: https://apidocs.bitrix24.com/api-reference/telephony/voximplant/users/index.html
    """

    @type_checker
    def activate_phone(
            self,
            user_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Activate user SIP device

        Documentation: https://apidocs.bitrix24.com/api-reference/telephony/voximplant/users/voximplant-user-activate-phone.html

        The method sets a flag indicating the presence of a SIP device for an employee.

        Args:
            user_id: User identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "USER_ID": user_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.activate_phone,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            user_id: Union[int, Iterable[int]],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get user settings

        Documentation: https://apidocs.bitrix24.com/api-reference/telephony/voximplant/users/voximplant-user-get.html

        The method returns user settings.

        Args:
            user_id: User ID or an array of user IDs;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if isinstance(user_id, int):
            api_user_id = user_id
        else:
            api_user_id = list(user_id)

        params: JSONDict = {
            "USER_ID": api_user_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )
