from typing import Annotated, Literal, Optional, Text, Union

from ....._constants import MISSING
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
        type: Annotated[Text, Literal["enum", "checkbox", "quantity"]],
        name: Text,
        *,
        active: Optional[Union[bool, B24BoolStrict]] = MISSING,
        code: Optional[Text] = MISSING,
        sort: Optional[int] = MISSING,
        description: Optional[Text] = MISSING,
        price: Optional[float] = MISSING,
        items: Optional[JSONList] = MISSING,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "DELIVERY_ID": delivery_id,
            "TYPE": type,
            "NAME": name,
        }

        if active is not MISSING:
            params["ACTIVE"] = B24BoolStrict(active).to_b24()

        if code is not MISSING:
            params["CODE"] = code

        if sort is not MISSING:
            params["SORT"] = sort

        if description is not MISSING:
            params["DESCRIPTION"] = description

        if price is not MISSING:
            params["PRICE"] = price

        if items is not MISSING:
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
        name: Optional[Text] = MISSING,
        active:  Optional[Union[bool, B24BoolStrict]] = MISSING,
        code: Optional[Text] = MISSING,
        sort: Optional[int] = MISSING,
        description: Optional[Text] = MISSING,
        price: Optional[float] = MISSING,
        items: Optional[JSONList] = MISSING,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "ID": bitrix_id,
        }

        if name is not MISSING:
            params["NAME"] = name

        if active is not MISSING:
            params["ACTIVE"] = B24BoolStrict(active).to_b24()

        if code is not MISSING:
            params["CODE"] = code

        if sort is not MISSING:
            params["SORT"] = sort

        if description is not MISSING:
            params["DESCRIPTION"] = description

        if price is not MISSING:
            params["PRICE"] = price

        if items is not MISSING:
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
