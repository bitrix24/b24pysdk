from typing import TYPE_CHECKING, Text

from ....bitrix_api.classes import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..base_crm import BaseCRM

if TYPE_CHECKING:
    from .userfield import Userfield


class Settings(BaseCRM):
    """"""

    def __init__(self, userfield: "Userfield"):
        super().__init__(scope=userfield._scope)
        self._path = self._get_path(userfield)

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

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.fields),
            params=params,
            timeout=timeout,
        )
