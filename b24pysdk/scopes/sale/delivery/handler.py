from typing import Optional, Text

from ...._constants import MISSING
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
        sort: Optional[int] = MISSING,
        description: Optional[Text] = MISSING,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "CODE": code,
            "NAME": name,
            "SETTINGS": settings,
            "PROFILES": profiles,
        }

        if sort is not MISSING:
            params["SORT"] = sort

        if description is not MISSING:
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
        code: Optional[Text] = MISSING,
        name: Optional[Text] = MISSING,
        sort: Optional[int] = MISSING,
        description: Optional[Text] = MISSING,
        settings: Optional[JSONDict] = MISSING,
        profiles: Optional[JSONList] = MISSING,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "ID": bitrix_id,
        }

        if code is not MISSING:
            params["CODE"] = code

        if name is not MISSING:
            params["NAME"] = name

        if sort is not MISSING:
            params["SORT"] = sort

        if description is not MISSING:
            params["DESCRIPTION"] = description

        if settings is not MISSING:
            params["SETTINGS"] = settings

        if profiles is not MISSING:
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
