from typing import Dict, Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Option",
]


class Option(BaseEntity):
    """Handle operations related to Bitrix24 user options.

    Documentation: https://apidocs.bitrix24.com/api-reference/common/settings/
    """

    @type_checker
    def get(
            self,
            *,
            option: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve the current value of a specified user option.

        Documentation: https://apidocs.bitrix24.com/api-reference/common/settings/user-option-get.html

        This method fetches the user-specific option's value bound to the application. If the parameter is not passed,
        it returns all recorded properties.

        Args:
            option: The name of the option to retrieve. One of the keys set by user.option.set. Optional.
            timeout: Timeout for the request in seconds.

        Returns:
            Instance of BitrixAPIRequest representing the ongoing request.
        """

        params: JSONDict = {}

        if option is not None:
            params["option"] = option

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set(
            self,
            options: Dict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Set values for one or more user options in Bitrix24.

        Documentation: https://apidocs.bitrix24.com/api-reference/common/settings/user-option-set.html

        This method associates data with the application and the user. If an option with a new key is passed, it will be
        recorded, and if an existing key is passed, its value will be updated.

        Args:
            options: Object format containing keys and values where keys are option names and values are their corresponding new settings. Required.
            timeout: Timeout for the request in seconds.

        Returns:
            Instance of BitrixAPIRequest representing the ongoing request.
        """

        params: JSONDict = {
            "options": options,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.set,
            params=params,
            timeout=timeout,
        )
