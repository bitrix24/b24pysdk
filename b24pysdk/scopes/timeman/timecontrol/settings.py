from typing import Annotated, Iterable, Literal, Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Settings",
]


class Settings(BaseEntity):
    """Class for managing settings of time tracking tool.

    Documentation: https://apidocs.bitrix24.com/api-reference/timeman/timecontrol/index.html
    """

    @type_checker
    def get(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get time control settings

        Documentation: https://apidocs.bitrix24.com/api-reference/timeman/timecontrol/timeman-timecontrol-settings-get.html

        The method retrieves the settings of the time control module.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            timeout=timeout,
        )

    @type_checker
    def set(  # noqa: C901, PLR0912
            self,
            *,
            active: Optional[bool] = MISSING,
            minimum_idle_for_report: Optional[int] = MISSING,
            register_offline: Optional[bool] = MISSING,
            register_idle: Optional[bool] = MISSING,
            register_desktop: Optional[bool] = MISSING,
            report_request_type: Optional[Annotated[Text, Literal["all", "user", "none"]]] = MISSING,
            report_request_users: Optional[Iterable[int]] = MISSING,
            report_simple_type: Optional[Annotated[Text, Literal["all", "user", "none"]]] = MISSING,
            report_simple_users: Optional[Iterable[int]] = MISSING,
            report_full_type: Optional[Annotated[Text, Literal["all", "user", "none"]]] = MISSING,
            report_full_users: Optional[Iterable[int]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Set time control settings

        Documentation; https://apidocs.bitrix24.com/api-reference/timeman/timecontrol/timeman-timecontrol-settings-set.html

        The method sets the configurations for the time control module.

        Args:
            active: Activate the time control module;

            minimum_idle_for_report: Minimum idle time in minutes after which a report is required;

            register_offline: Register offline status;

            register_idle: Register idle status;

            register_desktop: Register desktop application status;

            report_request_type: Report request type;

            report_request_users: Array of user IDs for whom report requests are required;

            report_simple_type: Type of simple report;

            report_simple_users: Array of user IDs with access to the simple report;

            report_full_type: Type of full report;

            report_full_users: Array of user IDs with access to the full report;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if active is not MISSING:
            params["ACTIVE"] = active

        if minimum_idle_for_report is not MISSING:
            params["MINIMUM_IDLE_FOR_REPORT"] = minimum_idle_for_report

        if register_offline is not MISSING:
            params["REGISTER_OFFLINE"] = register_offline

        if register_idle is not MISSING:
            params["REGISTER_IDLE"] = register_idle

        if register_desktop is not MISSING:
            params["REGISTER_DESKTOP"] = register_desktop

        if report_request_type is not MISSING:
            params["REPORT_REQUEST_TYPE"] = report_request_type

        if report_request_users is not MISSING:
            if report_request_users.__class__ is not list:
                report_request_users = list(report_request_users)

            params["REPORT_REQUEST_USERS"] = report_request_users

        if report_simple_type is not MISSING:
            params["REPORT_SIMPLE_TYPE"] = report_simple_type

        if report_simple_users is not MISSING:
            if report_simple_users.__class__ is not list:
                report_simple_users = list(report_simple_users)

            params["REPORT_SIMPLE_USERS"] = report_simple_users

        if report_full_type is not MISSING:
            params["REPORT_FULL_TYPE"] = report_full_type

        if report_full_users is not MISSING:
            if report_full_users.__class__ is not list:
                report_full_users = list(report_full_users)

            params["REPORT_FULL_USERS"] = report_full_users

        return self._make_bitrix_api_request(
            api_wrapper=self.set,
            params=params or None,
            timeout=timeout,
        )
