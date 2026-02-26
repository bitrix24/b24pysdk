from typing import Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Feature",
]


class Feature(BaseEntity):
    """"""

    @type_checker
    def access(
            self,
            group_id: int,
            feature: Text,
            operation: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "GROUP_ID": group_id,
            "FEATURE": feature,
            "OPERATION": operation,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.access,
            params=params,
            timeout=timeout,
        )
