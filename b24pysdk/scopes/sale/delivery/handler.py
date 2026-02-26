from typing import Optional, Text

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, JSONList, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Handler",
]


class Handler(BaseEntity):
    """"""

    @type_checker
    def add(
        self,
        code: Text,
        name: Text,
        settings: JSONDict,
        profiles: JSONList,
        *,
        sort: Optional[int] = None,
        description: Optional[Text] = None,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "CODE": code,
            "NAME": name,
            "SETTINGS": settings,
            "PROFILES": profiles,
        }

        if sort is not None:
            params["SORT"] = sort

        if description is not None:
            params["DESCRIPTION"] = description

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
        self,
        bitrix_id: int,
        *,
        code: Optional[Text] = None,
        name: Optional[Text] = None,
        sort: Optional[int] = None,
        description: Optional[Text] = None,
        settings: Optional[JSONDict] = None,
        profiles: Optional[JSONList] = None,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "ID": bitrix_id,
        }

        if code is not None:
            params["CODE"] = code

        if name is not None:
            params["NAME"] = name

        if sort is not None:
            params["SORT"] = sort

        if description is not None:
            params["DESCRIPTION"] = description

        if settings is not None:
            params["SETTINGS"] = settings

        if profiles is not None:
            params["PROFILES"] = profiles

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
        self,
        bitrix_id: int,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "ID": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
        self,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            timeout=timeout,
        )
