from typing import Text

from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ..._base_crm import BaseCRM

__all__ = [
    "Settings",
]


class Settings(BaseCRM):
    """"""

    @type_checker
    def fields(
            self,
            *,
            property_type: Text,
            user_type: Text,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "propertyType": property_type,
            "userType": user_type,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.fields,
            params=params,
            timeout=timeout,
        )
