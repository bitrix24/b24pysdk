from typing import Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Report",
]


class Report(BaseEntity):
    """Class for managing identified absences.

    Documentation: https://apidocs.bitrix24.com/api-reference/timeman/timecontrol/index.html
    """

    @type_checker
    def add(
            self,
            report_id: int,
            text: Text,
            *,
            user_id: Optional[int] = MISSING,
            type: Optional[Text] = MISSING,
            calendar: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add absence report

        Documentation: https://apidocs.bitrix24.com/api-reference/timeman/timecontrol/timeman-timecontrol-report-add.html

        The method sends an absence report and adds it to the calendar.

        Args:
            report_id: Identifier of the absence record;

            text: Report text;

            user_id: Identifier of the user;

            type: Report type;

            calendar: Flag for adding event to calendar;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "REPORT_ID": report_id,
            "TEXT": text,
        }

        if user_id is not MISSING:
            params["USER_ID"] = user_id

        if type is not MISSING:
            params["TYPE"] = type

        if calendar is not MISSING:
            params["CALENDAR"] = calendar

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )
