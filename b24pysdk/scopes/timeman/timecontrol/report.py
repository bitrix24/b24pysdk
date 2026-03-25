from typing import Optional, Text

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Report",
]


class Report(BaseEntity):
    """"""

    @type_checker
    def add(
            self,
            report_id: int,
            text: Text,
            *,
            user_id: Optional[int] = None,
            type: Optional[Text] = None,
            calendar: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "REPORT_ID": report_id,
            "TEXT": text,
        }

        if user_id is not None:
            params["USER_ID"] = user_id

        if type is not None:
            params["TYPE"] = type

        if calendar is not None:
            params["CALENDAR"] = calendar

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )
