from typing import Annotated, Text

from ....api.requests import BitrixAPIValueRequest
from ....schemas.crm.userfield import CRMUserfieldFieldsData, CRMUserfieldFieldsDict
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout, UserTypeIDLiteral
from .._base_crm import BaseCRM

__all__ = [
    "Settings",
]


class Settings(BaseCRM):
    """"""

    @type_checker
    def fields(
            self,
            type: Annotated[Text, UserTypeIDLiteral],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIValueRequest[CRMUserfieldFieldsData, CRMUserfieldFieldsDict]:
        """Get the settings description.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/user-defined-fields/crm-userfield-settings-fields.html

        The method returns the description of the settings fields for the custom field type

        Args:
            type: The type of the custom field type;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "type": type,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.fields,
            params=params,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValueRequest,
            result_adapter=CRMUserfieldFieldsDict.from_bitrix,
        )
