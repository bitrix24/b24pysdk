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

        return self._make_bitrix_api_request(
            api_method=self.fields,
            params=params,
            timeout=timeout,
        )
