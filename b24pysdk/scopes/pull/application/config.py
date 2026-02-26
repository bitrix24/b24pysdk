from typing import Optional

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import B24Bool, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Config",
]


class Config(BaseEntity):
    """"""

    @type_checker
    def get(
            self,
            *,
            cache: Optional[bool] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if cache is not None:
            params["CACHE"] = B24Bool(cache).to_b24()

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params or None,
            timeout=timeout,
        )
