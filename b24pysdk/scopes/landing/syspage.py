from typing import Optional, Text, Union

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import B24BoolStrict, JSONDict, Timeout
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
            active: Optional[Union[bool, B24BoolStrict]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
        }

        if active is not None:
            params["active"] = B24BoolStrict(active).to_b24()

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
            additional: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "siteId": site_id,
            "type": type,
        }

        if additional is not None:
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
            lid: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
            "type": type,
        }

        if lid is not None:
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
