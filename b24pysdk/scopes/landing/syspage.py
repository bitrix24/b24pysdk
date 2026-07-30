from typing import Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.converters import bool_to_bitrix
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "SysPage",
]


class SysPage(BaseEntity):
    """"""

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            active: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
        }

        if active is not MISSING:
            params["active"] = bool_to_bitrix(active, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def get_special_page(
            self,
            site_id: int,
            type: Text,
            *,
            additional: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "siteId": site_id,
            "type": type,
        }

        if additional is not MISSING:
            params["additional"] = additional

        return self._make_bitrix_api_request(
            api_wrapper=self.get_special_page,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set(
            self,
            bitrix_id: int,
            type: Text,
            *,
            lid: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
            "type": type,
        }

        if lid is not MISSING:
            params["lid"] = lid

        return self._make_bitrix_api_request(
            api_wrapper=self.set,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete_for_site(
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
            api_wrapper=self.delete_for_site,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete_for_landing(
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
            api_wrapper=self.delete_for_landing,
            params=params,
            timeout=timeout,
        )
