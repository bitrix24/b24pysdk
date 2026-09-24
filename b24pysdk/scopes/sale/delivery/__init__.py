from functools import cached_property
from typing import Iterable, Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.converters import bool_to_bitrix
from ....utils.functional import type_checker
from ....utils.types import JSONDict, JSONList, Timeout
from ..._base_entity import BaseEntity
from .config import Config
from .extra import Extra
from .handler import Handler
from .request import Request

__all__ = [
    "Delivery",
]


class Delivery(BaseEntity):
    """"""

    @cached_property
    def config(self) -> Config:
        """"""
        return Config(self)

    @cached_property
    def extra(self) -> Extra:
        """"""
        return Extra(self)

    @cached_property
    def handler(self) -> Handler:
        """"""
        return Handler(self)

    @cached_property
    def request(self) -> Request:
        """"""
        return Request(self)

    @type_checker
    def add(
        self,
        rest_code: Text,
        name: Text,
        currency: Text,
        *,
        description: Optional[Text] = MISSING,
        sort: Optional[int] = MISSING,
        active: Optional[bool] = MISSING,
        config: Optional[JSONList] = MISSING,
        logotype: Text = MISSING,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "REST_CODE": rest_code,
            "NAME": name,
            "CURRENCY": currency,
        }

        if description is not MISSING:
            params["DESCRIPTION"] = description

        if sort is not MISSING:
            params["SORT"] = sort

        if active is not MISSING:
            params["ACTIVE"] = bool_to_bitrix(active, is_required=True)

        if config is not MISSING:
            params["CONFIG"] = config

        if logotype is not MISSING:
            params["LOGOTYPE"] = logotype

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
        name: Optional[Text] = MISSING,
        currency: Optional[Text] = MISSING,
        description: Optional[Text] = MISSING,
        sort: Optional[int] = MISSING,
        active: Optional[bool] = MISSING,
        logotype: Text = MISSING,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        fields: JSONDict = {}

        if name is not MISSING:
            fields["NAME"] = name

        if currency is not MISSING:
            fields["CURRENCY"] = currency

        if description is not MISSING:
            fields["DESCRIPTION"] = description

        if sort is not MISSING:
            fields["SORT"] = sort

        if active is not MISSING:
            fields["ACTIVE"] = bool_to_bitrix(active, is_required=True)

        if logotype is not MISSING:
            fields["LOGOTYPE"] = logotype

        params: JSONDict = {
            "ID": bitrix_id,
            "FIELDS": fields,
        }

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
    def getlist(
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
            api_wrapper=self.getlist,
            params=params,
            timeout=timeout,
        )
