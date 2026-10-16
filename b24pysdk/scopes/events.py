from typing import List, Text

from .._constants import MISSING
from ..api.requests import BitrixAPIRequest
from ..utils.functional import type_checker
from ..utils.types import JSONDict, Timeout
from ._base_scope import BaseScope

__all__ = [
    "Events",
]


class Events(BaseScope):
    """Class for retrieving a list of available events.

    Documentaiton: https://apidocs.bitrix24.com/api-reference/events/index.html
    """

    @type_checker
    def __call__(
            self,
            scope: Text = MISSING,
            full: bool = MISSING,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[List[Text]]:
        """Get a list of available events

        Documentation: https://apidocs.bitrix24.com/api-reference/events/events.html

        The method returns a comprehensive list of available events.

        Args:
            scope: The method will return events belonging to the specified permission;

            full: The method will return the complete list of events;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if scope is not MISSING:
            params["SCOPE"] = scope

        if full is not MISSING:
            params["FULL"] = full

        return self._make_bitrix_api_request(
            api_wrapper=self,
            params=params,
            timeout=timeout,
        )
