from typing import Iterable, Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Role",
]


class Role(BaseEntity):
    """"""

    @type_checker
    def enable(
            self,
            mode: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "mode": mode,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.enable,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def is_enabled(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        return self._make_bitrix_api_request(
            api_wrapper=self.is_enabled,
            params=None,
            timeout=timeout,
        )

    @type_checker
    def get_list(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        return self._make_bitrix_api_request(
            api_wrapper=self.get_list,
            params=None,
            timeout=timeout,
        )

    @type_checker
    def get_rights(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get_rights,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set_rights(
            self,
            bitrix_id: int,
            rights: JSONDict,
            *,
            additional: Optional[Iterable[Text]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if additional is not MISSING and additional.__class__ is not list:
            additional = list(additional)

        params: JSONDict = {
            "id": bitrix_id,
            "rights": rights,
        }

        if additional is not MISSING:
            params["additional"] = additional

        return self._make_bitrix_api_request(
            api_wrapper=self.set_rights,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set_access_codes(
            self,
            bitrix_id: int,
            *,
            codes: Optional[Iterable[Text]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
        }

        if codes is not MISSING:
            if codes.__class__ is not list:
                codes = list(codes)

            params["codes"] = codes

        return self._make_bitrix_api_request(
            api_wrapper=self.set_access_codes,
            params=params,
            timeout=timeout,
        )
