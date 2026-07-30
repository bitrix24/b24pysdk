from functools import cached_property
from typing import Iterable, Optional, Text, Union

from ...._constants import MISSING
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
        ofd: Optional[Text] = MISSING,
        ofd_settings: Optional[JSONDict] = MISSING,
        number_kkm: Optional[Text] = MISSING,
        active: Optional[Union[bool, B24BoolStrict]] = MISSING,
        sort: Optional[int] = MISSING,
        use_offline: Optional[Union[bool, B24BoolStrict]] = MISSING,
        settings: Optional[JSONDict] = MISSING,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "NAME": name,
            "REST_CODE": rest_code,
            "EMAIL": email,
        }

        if ofd is not MISSING:
            params["OFD"] = ofd

        if ofd_settings is not MISSING:
            params["OFD_SETTINGS"] = ofd_settings

        if number_kkm is not MISSING:
            params["NUMBER_KKM"] = number_kkm

        if active is not MISSING:
            params["ACTIVE"] = B24BoolStrict(active).to_b24()

        if sort is not MISSING:
            params["SORT"] = sort

        if use_offline is not MISSING:
            params["USE_OFFLINE"] = B24BoolStrict(use_offline).to_b24()

        if settings is not MISSING:
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
        select: Optional[Iterable[Text]] = MISSING,
        filter: Optional[JSONDict] = MISSING,
        order: Optional[JSONDict] = MISSING,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {}

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)
            params["SELECT"] = select

        if filter is not MISSING:
            params["FILTER"] = filter

        if order is not MISSING:
            params["ORDER"] = order

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

        params: JSONDict = {
            "ID": bitrix_id,
            "FIELDS": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
