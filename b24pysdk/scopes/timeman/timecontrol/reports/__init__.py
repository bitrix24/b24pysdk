from functools import cached_property
from typing import Optional

from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity
from .settings import Settings
from .users import Users

__all__ = [
    "Reports",
]


class Reports(BaseEntity):
    """"""

    @cached_property
    def settings(self) -> Settings:
        """"""
        return Settings(self)

    @cached_property
    def users(self) -> Users:
        """"""
        return Users(self)

    @type_checker
    def get(
            self,
            user_id: int,
            month: int,
            year: int,
            *,
            idle_minutes: Optional[int] = None,
            workday_hours: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "USER_ID": user_id,
            "MONTH": month,
            "YEAR": year,
        }

        if idle_minutes is not None:
            params["IDLE_MINUTES"] = idle_minutes

        if workday_hours is not None:
            params["WORKDAY_HOURS"] = workday_hours

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )
