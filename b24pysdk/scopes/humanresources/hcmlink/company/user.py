from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, JSONList, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "User",
]


class User(BaseEntity):
    """"""

    @type_checker
    def list(
            self,
            *,
            limit: int = MISSING,
            offset: int = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONList]:
        """"""

        params: JSONDict = {}

        if limit is not MISSING:
            params["limit"] = limit

        if offset is not MISSING:
            params["offset"] = offset

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params or None,
            timeout=timeout,
        )
