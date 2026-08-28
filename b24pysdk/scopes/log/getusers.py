from typing import Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import classproperty, type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Getusers",
]


class Getusers(BaseEntity):
    """Class for checking important message readers.

    Documentation: https://apidocs.bitrix24.com/api-reference/log/index.html
    """

    @classproperty
    def _name(cls) -> Text:
        """"""
        return "getusers"

    @type_checker
    def important(
            self,
            post_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """View users who read an important message

        Documentation: https://apidocs.bitrix24.com/api-reference/log/log-blogpost-getusers-important.html

        The method returns an array of user IDs who have read an important message.

        Args:
            post_id: The identifier of the important message in the News Feed;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "POST_ID": post_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.important,
            params=params,
            timeout=timeout,
        )
