from functools import cached_property
from typing import Iterable, Optional, Text, Union

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

    @type_checker
    def get(
            self,
            department_ids: Iterable[Union[int, Text]],
            *,
            user_data: Optional[Union[bool, B24BoolStrict]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if department_ids.__class__ is not list:
            department_ids = list(department_ids)

        params = dict(
            ID=department_ids,
        )

        if user_data is not None:
            params["USER_DATA"] = B24BoolStrict(user_data).to_b24()

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @cached_property
    def managers(self) -> Managers:
        """"""
        return Managers(self)
