from functools import cached_property
from typing import Iterable, Optional, Text, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import B24BoolStrict, JSONDict, JSONList, Timeout
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
    def extra_service(self) -> Extra:
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
        description: Optional[Text] = None,
        sort: Optional[int] = None,
        active: Optional[Union[bool, B24BoolStrict]] = None,
        config: Optional[JSONList] = None,
        logotype: Optional[Text] = None,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "REST_CODE": rest_code,
            "NAME": name,
            "CURRENCY": currency,
        }

        if description is not None:
            params["DESCRIPTION"] = description

        if sort is not None:
            params["SORT"] = sort

        if active is not None:
            params["ACTIVE"] = B24BoolStrict(active).to_b24()

        if config is not None:
            params["CONFIG"] = config

        if logotype is not None:
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
        name: Optional[Text] = None,
        currency: Optional[Text] = None,
        description: Optional[Text] = None,
        sort: Optional[int] = None,
        active: Optional[Union[bool, B24BoolStrict]] = None,
        logotype: Optional[Text] = None,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        fields: JSONDict = {}

        if name is not None:
            fields["NAME"] = name

        if currency is not None:
            fields["CURRENCY"] = currency

        if description is not None:
            fields["DESCRIPTION"] = description

        if sort is not None:
            fields["SORT"] = sort

        if active is not None:
            fields["ACTIVE"] = B24BoolStrict(active).to_b24()

        if logotype is not None:
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
        select: Optional[Iterable[Text]] = None,
        filter: Optional[JSONDict] = None,
        order: Optional[JSONDict] = None,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {}

        if select is not None:
            if select.__class__ is not list:
                select = list(select)
            params["SELECT"] = select

        if filter is not None:
            params["FILTER"] = filter

        if order is not None:
            params["ORDER"] = order

        return self._make_bitrix_api_request(
            api_wrapper=self.getlist,
            params=params,
            timeout=timeout,
        )
