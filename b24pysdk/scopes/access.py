from typing import Iterable, Text

from ..api.requests import BitrixAPIValueRequest
from ..schemas.access import AccessNamesData, AccessNamesDict
from ..utils.functional import type_checker
from ..utils.types import JSONDict, Timeout
from ._adapters import BitrixSchemaDictAdapter
from ._base_scope import BaseScope

__all__ = [
    "Access",
]


class Access(BaseScope):
    """CLass for retrieving names of access codes.

    Documentation: https://apidocs.bitrix24.com/api-reference/common/system/index.html
    """

    @type_checker
    def name(
            self,
            access: Iterable[Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIValueRequest[AccessNamesData, AccessNamesDict]:
        """Get access permission names

        Documentation: https://apidocs.bitrix24.com/api-reference/common/system/access-name.html

        The  method retrieves the names of access permissions.

        Args:
            access: List of access codes for which names need to be retrieved;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if access.__class__ is not list:
            access = list(access)

        params: JSONDict = {
            "ACCESS": access,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.name,
            params=params,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValueRequest,
            result_adapter=BitrixSchemaDictAdapter(AccessNamesDict),
        )
