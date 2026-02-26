from functools import cached_property
from typing import Iterable, Optional, Text, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import B24BoolStrict, JSONDict, Timeout
from ..._base_entity import BaseEntity
from .check import Check
from .handler import Handler

__all__ = [
    "Cashbox",
]


class Cashbox(BaseEntity):
    """"""

    @cached_property
    def check(self) -> Check:
        """"""
        return Check(self)

    @cached_property
    def handler(self) -> Handler:
        """"""
        return Handler(self)

    @type_checker
    def add(
        self,
        name: Text,
        rest_code: Text,
        email: Text,
        *,
        ofd: Optional[Text] = None,
        ofd_settings: Optional[JSONDict] = None,
        number_kkm: Optional[Text] = None,
        active: Optional[Union[bool, B24BoolStrict]] = None,
        sort: Optional[int] = None,
        use_offline: Optional[Union[bool, B24BoolStrict]] = None,
        settings: Optional[JSONDict] = None,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = dict()
        params["NAME"] = name
        params["REST_CODE"] = rest_code
        params["EMAIL"] = email

        if ofd is not None:
            params["OFD"] = ofd

        if ofd_settings is not None:
            params["OFD_SETTINGS"] = ofd_settings

        if number_kkm is not None:
            params["NUMBER_KKM"] = number_kkm

        if active is not None:
            params["ACTIVE"] = B24BoolStrict(active).to_b24()

        if sort is not None:
            params["SORT"] = sort

        if use_offline is not None:
            params["USE_OFFLINE"] = B24BoolStrict(use_offline).to_b24()

        if settings is not None:
            params["SETTINGS"] = settings

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
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

        params: JSONDict = dict()
        params["ID"] = bitrix_id

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
        self,
        *,
        select: Optional[Iterable[Text]] = None,
        filter: Optional[JSONDict] = None,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = dict()

        if select is not None:
            if select.__class__ is not list:
                select = list(select)
            params["SELECT"] = select

        if filter is not None:
            params["FILTER"] = filter

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
        self,
        bitrix_id: int,
        fields: JSONDict,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = dict()
        params["ID"] = bitrix_id
        params["FIELDS"] = fields

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
