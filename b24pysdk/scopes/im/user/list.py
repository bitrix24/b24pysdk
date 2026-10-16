from typing import Iterable, Optional, Text, Union

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.converters import bool_to_bitrix
from ....utils.functional import type_checker
from ....utils.types import JSONDict, JSONList, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "List",
]


class List(BaseEntity):
    """Class for retrieving data about users.

    Documentation: https://apidocs.bitrix24.com/api-reference/chats/users/index.html
    """

    @type_checker
    def get(
            self,
            bitrix_id: Iterable[Union[int, Text]],
            *,
            avatar_hr: Optional[bool] = MISSING,
            result_type: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[Union[JSONDict, JSONList]]:
        """Get user data

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/users/im-user-list-get.html

        The method returns data about users based on a list of identifiers.

        Args:
            bitrix_id: An array of user identifiers or a JSON string containing an array;

            avatar_hr: Parameter to request the avatar_hr field with the high-resolution avatar URL;

            result_type: Format of the result;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if bitrix_id.__class__ is not list:
            bitrix_id = list(bitrix_id)

        params = {
            "ID": bitrix_id,
        }

        if avatar_hr is not MISSING:
            params["AVATAR_HR"] = bool_to_bitrix(avatar_hr, is_required=True)

        if result_type is not MISSING:
            params["RESULT_TYPE"] = result_type

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )
