from functools import cached_property
from typing import Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Number, Timeout
from .._base_scope import BaseScope
from .networkrange import Networkrange
from .schedule import Schedule
from .timecontrol import Timecontrol

__all__ = [
    "Timeman",
]


class Timeman(BaseScope):
    """Class for managing the workday.

    Documentation: https://apidocs.bitrix24.com/api-reference/timeman/base/index.html
    """

    @cached_property
    def networkrange(self) -> Networkrange:
        """"""
        return Networkrange(self)

    @cached_property
    def schedule(self) -> Schedule:
        """"""
        return Schedule(self)

    @cached_property
    def timecontrol(self) -> Timecontrol:
        """"""
        return Timecontrol(self)

    @type_checker
    def close(
            self,
            *,
            user_id: Optional[int] = MISSING,
            time: Optional[Text] = MISSING,
            report: Optional[Text] = MISSING,
            lat: Optional[Number] = MISSING,
            lon: Optional[Number] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Close current day

        Documentation: https://apidocs.bitrix24.com/api-reference/timeman/base/timeman-close.html

        The method ends the current workday.

        Args:
            user_id: User identifier;

            time: The end time and date of the workday in the ATOM format;

            report: Reason for changing the workday;

            lat: Geographic latitude of the end of the workday;

            lon: Geographic longitude of the end of the workday;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if user_id is not MISSING:
            params["USER_ID"] = user_id

        if time is not MISSING:
            params["TIME"] = time

        if report is not MISSING:
            params["REPORT"] = report

        if lat is not MISSING:
            params["LAT"] = lat

        if lon is not MISSING:
            params["LON"] = lon

        return self._make_bitrix_api_request(
            api_wrapper=self.close,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def open(
            self,
            *,
            user_id: Optional[int] = MISSING,
            time: Optional[Text] = MISSING,
            report: Optional[Text] = MISSING,
            lat: Optional[Number] = MISSING,
            lon: Optional[Number] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Start a new workday

        Documentation: https://apidocs.bitrix24.com/api-reference/timeman/base/timeman-open.html

        The method starts a new workday or continues the workday after a break or completion.

        Args:
            user_id: User identifier;

            time: The start date and time of the workday in the ATOM format;

            report: Reason for changing the workday;

            lat: Geographic latitude of the end of the workday;

            lon: Geographic longitude of the end of the workday;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if user_id is not MISSING:
            params["USER_ID"] = user_id

        if time is not MISSING:
            params["TIME"] = time

        if report is not MISSING:
            params["REPORT"] = report

        if lat is not MISSING:
            params["LAT"] = lat

        if lon is not MISSING:
            params["LON"] = lon

        return self._make_bitrix_api_request(
            api_wrapper=self.open,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def pause(
            self,
            *,
            user_id: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Pause the current workday

        Documentation: https://apidocs.bitrix24.com/api-reference/timeman/base/timeman-pause.html

        The method pauses the current workday.

        Args:
            user_id: User identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if user_id is not MISSING:
            params["USER_ID"] = user_id

        return self._make_bitrix_api_request(
            api_wrapper=self.pause,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def settings(
            self,
            *,
            user_id: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get user work time settings

        Documentation: https://apidocs.bitrix24.com/api-reference/timeman/base/timeman-settings.html

        The method retrieves the user's work time settings.

        Args:
            user_id: User identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if user_id is not MISSING:
            params["USER_ID"] = user_id

        return self._make_bitrix_api_request(
            api_wrapper=self.settings,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def status(
            self,
            *,
            user_id: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get information about the current workday

        Documentation: https://apidocs.bitrix24.com/api-reference/timeman/base/timeman-status.html

        The method retrieves information about the current workday.

        Args:
            user_id: User identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if user_id is not MISSING:
            params["USER_ID"] = user_id

        return self._make_bitrix_api_request(
            api_wrapper=self.status,
            params=params or None,
            timeout=timeout,
        )
