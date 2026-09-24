from functools import cached_property
from typing import Iterable, Optional

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.converters import bool_to_bitrix
from ....utils.functional import type_checker
from ....utils.types import JSONList, Timeout
from ..._base_entity import BaseEntity
from .colleagues import Colleagues
from .employees import Employees
from .managers import Managers

__all__ = [
    "Department",
]


class Department(BaseEntity):
    """"""

    @cached_property
    def colleagues(self) -> Colleagues:
        """"""
        return Colleagues(self)

    @cached_property
    def employees(self) -> Employees:
        """"""
        return Employees(self)

    @cached_property
    def managers(self) -> Managers:
        """"""
        return Managers(self)

    @type_checker
    def get(
            self,
            bitrix_id: Iterable[int],
            *,
            user_data: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONList]:
        """"""

        if bitrix_id.__class__ is not list:
            bitrix_id = list(bitrix_id)

        params = dict(
            ID=bitrix_id,
        )

        if user_data is not MISSING:
            params["USER_DATA"] = bool_to_bitrix(user_data, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )
