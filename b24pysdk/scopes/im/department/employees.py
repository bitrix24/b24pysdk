from typing import Iterable, Optional, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import B24BoolStrict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Employees",
]


class Employees(BaseEntity):
    """"""

    @type_checker
    def get(
            self,
            bitrix_id: Iterable[int],
            *,
            user_data: Optional[Union[bool, B24BoolStrict]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if bitrix_id.__class__ is not list:
            bitrix_id = list(bitrix_id)

        params = dict(
            ID=bitrix_id,
        )

        if user_data is not None:
            params["USER_DATA"] = B24BoolStrict(user_data).to_b24()

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )
