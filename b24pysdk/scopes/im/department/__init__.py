from functools import cached_property
from typing import Iterable, Optional, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import B24BoolStrict, Timeout
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
