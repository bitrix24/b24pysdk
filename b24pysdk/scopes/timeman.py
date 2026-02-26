from typing import Optional, Text

from ..api.requests import BitrixAPIRequest
from ..utils.functional import type_checker
from ..utils.types import Number, Timeout
from ._base_scope import BaseScope

__all__ = [
    "Timeman",
]


class Timeman(BaseScope):
    """"""

    @type_checker
    def close(
            self,
            *,
            user_id: Optional[int] = None,
            time: Optional[Text] = None,
            report: Optional[Text] = None,
            lat: Optional[Number] = None,
            lon: Optional[Number] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if user_id is not None:
            params["USER_ID"] = user_id

        if time is not None:
            params["TIME"] = time

        if report is not None:
            params["REPORT"] = report

        if lat is not None:
            params["LAT"] = lat

        if lon is not None:
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
            user_id: Optional[int] = None,
            time: Optional[Text] = None,
            report: Optional[Text] = None,
            lat: Optional[Number] = None,
            lon: Optional[Number] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if user_id is not None:
            params["USER_ID"] = user_id

        if time is not None:
            params["TIME"] = time

        if report is not None:
            params["REPORT"] = report

        if lat is not None:
            params["LAT"] = lat

        if lon is not None:
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
            user_id: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if user_id is not None:
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
            user_id: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if user_id is not None:
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
            user_id: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if user_id is not None:
            params["USER_ID"] = user_id

        return self._make_bitrix_api_request(
            api_wrapper=self.status,
            params=params or None,
            timeout=timeout,
        )
