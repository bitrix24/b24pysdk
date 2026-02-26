from typing import Optional, Text, Union

from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import B24BoolStrict, JSONDict, JSONList, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "Service",
]


class Service(BaseEntity):
    """"""

    @type_checker
    def add(
        self,
        delivery_id: int,
        type: Text,
        name: Text,
        *,
        active: Optional[Union[bool, B24BoolStrict]] = None,
        code: Optional[Text] = None,
        sort: Optional[int] = None,
        description: Optional[Text] = None,
        price: Optional[float] = None,
        items: Optional[JSONList] = None,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "DELIVERY_ID": delivery_id,
            "TYPE": type,
            "NAME": name,
        }

        if active is not None:
            params["ACTIVE"] = B24BoolStrict(active).to_b24()

        if code is not None:
            params["CODE"] = code

        if sort is not None:
            params["SORT"] = sort

        if description is not None:
            params["DESCRIPTION"] = description

        if price is not None:
            params["PRICE"] = price

        if items is not None:
            params["ITEMS"] = items

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
        active:  Optional[Union[bool, B24BoolStrict]] = None,
        code: Optional[Text] = None,
        sort: Optional[int] = None,
        description: Optional[Text] = None,
        price: Optional[float] = None,
        items: Optional[JSONList] = None,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "ID": bitrix_id,
        }

        if name is not None:
            params["NAME"] = name

        if active is not None:
            params["ACTIVE"] = B24BoolStrict(active).to_b24()

        if code is not None:
            params["CODE"] = code

        if sort is not None:
            params["SORT"] = sort

        if description is not None:
            params["DESCRIPTION"] = description

        if price is not None:
            params["PRICE"] = price

        if items is not None:
            params["ITEMS"] = items

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
        self,
        delivery_id: int,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "DELIVERY_ID": delivery_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
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
