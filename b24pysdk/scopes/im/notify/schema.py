from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Schema",
]


class Schema(BaseEntity):
    """"""

    @type_checker
    def get(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """"""

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            timeout=timeout,
        )
