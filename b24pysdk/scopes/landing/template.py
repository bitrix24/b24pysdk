from typing import Optional

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Template",
]


class Template(BaseEntity):
    """"""

    @type_checker
    def getlist(
            self,
            *,
            params: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        api_params = dict()

        if params is not None:
            api_params["params"] = params

        return self._make_bitrix_api_request(
            api_wrapper=self.getlist,
            params=api_params or None,
            timeout=timeout,
        )

    @type_checker
    def get_landing_ref(
            self,
            bitrix_id: int,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get_landing_ref,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_site_ref(
            self,
            bitrix_id: int,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get_site_ref,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set_landing_ref(
            self,
            bitrix_id: int,
            *,
            data: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
        }

        if data is not None:
            params["data"] = data

        return self._make_bitrix_api_request(
            api_wrapper=self.set_landing_ref,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set_site_ref(
            self,
            bitrix_id: int,
            *,
            data: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
        }

        if data is not None:
            params["data"] = data

        return self._make_bitrix_api_request(
            api_wrapper=self.set_site_ref,
            params=params,
            timeout=timeout,
        )
