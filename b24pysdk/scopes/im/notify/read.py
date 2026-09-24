from typing import Iterable, Optional

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.converters import bool_to_bitrix
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Read",
]


class Read(BaseEntity):
    """"""

    @type_checker
    def __call__(
            self,
            bitrix_id: int,
            *,
            action: Optional[bool] = MISSING,
            only_current: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """"""

        params = {
            "ID": bitrix_id,
        }

        if action is not MISSING:
            params["ACTION"] = bool_to_bitrix(action, is_required=True)

        if only_current is not MISSING:
            params["ONLY_CURRENT"] = bool_to_bitrix(only_current, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            ids: Iterable[int],
            *,
            action: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """"""

        if ids.__class__ is not list:
            ids = list(ids)

        params = {
            "IDS": ids,
        }

        if action is not MISSING:
            params["ACTION"] = bool_to_bitrix(action, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def all(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """"""

        return self._make_bitrix_api_request(
            api_wrapper=self.all,
            timeout=timeout,
        )
