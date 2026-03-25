from typing import Annotated, Iterable, Literal, Optional, Text

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Settings",
]


class Settings(BaseEntity):
    """"""

    @type_checker
    def get(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            timeout=timeout,
        )

    @type_checker
    def set(  # noqa: C901, PLR0912
            self,
            *,
            active: Optional[bool] = None,
            minimum_idle_for_report: Optional[int] = None,
            register_offline: Optional[bool] = None,
            register_idle: Optional[bool] = None,
            register_desktop: Optional[bool] = None,
            report_request_type: Optional[Annotated[Text, Literal["all", "user", "none"]]] = None,
            report_request_users: Optional[Iterable[int]] = None,
            report_simple_type: Optional[Annotated[Text, Literal["all", "user", "none"]]] = None,
            report_simple_users: Optional[Iterable[int]] = None,
            report_full_type: Optional[Annotated[Text, Literal["all", "user", "none"]]] = None,
            report_full_users: Optional[Iterable[int]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {}

        if active is not None:
            params["ACTIVE"] = active

        if minimum_idle_for_report is not None:
            params["MINIMUM_IDLE_FOR_REPORT"] = minimum_idle_for_report

        if register_offline is not None:
            params["REGISTER_OFFLINE"] = register_offline

        if register_idle is not None:
            params["REGISTER_IDLE"] = register_idle

        if register_desktop is not None:
            params["REGISTER_DESKTOP"] = register_desktop

        if report_request_type is not None:
            params["REPORT_REQUEST_TYPE"] = report_request_type

        if report_request_users is not None:
            if report_request_users.__class__ is not list:
                report_request_users = list(report_request_users)

            params["REPORT_REQUEST_USERS"] = report_request_users

        if report_simple_type is not None:
            params["REPORT_SIMPLE_TYPE"] = report_simple_type

        if report_simple_users is not None:
            if report_simple_users.__class__ is not list:
                report_simple_users = list(report_simple_users)

            params["REPORT_SIMPLE_USERS"] = report_simple_users

        if report_full_type is not None:
            params["REPORT_FULL_TYPE"] = report_full_type

        if report_full_users is not None:
            if report_full_users.__class__ is not list:
                report_full_users = list(report_full_users)

            params["REPORT_FULL_USERS"] = report_full_users

        return self._make_bitrix_api_request(
            api_wrapper=self.set,
            params=params or None,
            timeout=timeout,
        )
