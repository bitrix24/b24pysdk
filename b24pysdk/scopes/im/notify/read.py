from typing import Iterable, Optional, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import B24BoolStrict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Read",
]


class Read(BaseEntity):
    """"""

    @type_checker
    def list(
            self,
            ids: Iterable[int],
            *,
            action: Optional[Union[bool, B24BoolStrict]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if ids.__class__ is not list:
            ids = list(ids)

        params = {
            "IDS": ids,
        }

        if action is not None:
            params["ACTION"] = B24BoolStrict(action).to_b24()

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def read(
            self,
            bitrix_id: int,
            *,
            only_current: Optional[Union[bool, B24BoolStrict]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "ID": bitrix_id,
        }

        if only_current is not None:
            params["ONLY_CURRENT"] = B24BoolStrict(only_current).to_b24()

        return self._make_bitrix_api_request(
            api_wrapper=self.read,
            params=params,
            timeout=timeout,
        )
