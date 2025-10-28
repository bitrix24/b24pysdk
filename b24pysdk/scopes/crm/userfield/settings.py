from typing import Text

from ....bitrix_api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from .._base_crm import BaseCRM

__all__ = [
    "Settings",
]


class Settings(BaseCRM):
    """"""

    @type_checker
    def fields(
            self,
            *,
            type: Text,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the settings description.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/user-defined-fields/crm-userfield-settings-fields.html

        The method returns the description of the settings fields for the custom field type

        Args:
            type: The type of the custom field type;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "type": type,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.fields,
            params=params,
            timeout=timeout,
        )
