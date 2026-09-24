from functools import cached_property
from typing import Optional

from ....._constants import MISSING
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
    """Methods for working with reports on an employee's absences.

    Documentation: https://apidocs.bitrix24.com/api-reference/timeman/timecontrol/index.html
    """

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
            idle_minutes: Optional[int] = MISSING,
            workday_hours: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get report on identified absences

        Documentation: https://apidocs.bitrix24.com/api-reference/timeman/timecontrol/timeman-timecontrol-reports-get.html

        The method retrieves a report on identified absences.

        Args:
            user_id: User ID for whom the reports are requested;

            month: Month number;

            year: Year;

            idle_minutes: Maximum time of absence at the workplace that is not counted as absence;

            workday_hours: Duration of the workday in hours;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "USER_ID": user_id,
            "MONTH": month,
            "YEAR": year,
        }

        if idle_minutes is not MISSING:
            params["IDLE_MINUTES"] = idle_minutes

        if workday_hours is not MISSING:
            params["WORKDAY_HOURS"] = workday_hours

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )
