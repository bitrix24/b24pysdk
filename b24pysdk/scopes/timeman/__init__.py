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
    """"""

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
        """"""

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
        """"""

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
        """"""

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
        """"""

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
        """"""

        params: JSONDict = {}

        if user_id is not MISSING:
            params["USER_ID"] = user_id

        return self._make_bitrix_api_request(
            api_wrapper=self.status,
            params=params or None,
            timeout=timeout,
        )
