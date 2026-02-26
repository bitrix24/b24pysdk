from typing import Optional, Text, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import B24BoolStrict, JSONDict, JSONList, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Request",
]


class Request(BaseEntity):
    """"""

    @type_checker
    def update(
        self,
        delivery_id: int,
        request_id: Text,
        *,
        finalize: Optional[Union[bool, B24BoolStrict]] = None,
        status: Optional[JSONDict] = None,
        properties: Optional[JSONList] = None,
        overwrite_properties: Optional[Union[bool, B24BoolStrict]] = None,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "DELIVERY_ID": delivery_id,
            "REQUEST_ID": request_id,
        }

        if finalize is not None:
            params["FINALIZE"] = B24BoolStrict(finalize).to_b24()

        if status is not None:
            params["STATUS"] = status

        if properties is not None:
            params["PROPERTIES"] = properties

        if overwrite_properties is not None:
            params["OVERWRITE_PROPERTIES"] = B24BoolStrict(overwrite_properties).to_b24()

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def sendmessage(
        self,
        delivery_id: int,
        request_id: Text,
        addressee: Text,
        message: JSONDict,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "DELIVERY_ID": delivery_id,
            "REQUEST_ID": request_id,
            "ADDRESSEE": addressee,
            "MESSAGE": message,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.sendmessage,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
        self,
        delivery_id: int,
        request_id: Text,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "DELIVERY_ID": delivery_id,
            "REQUEST_ID": request_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )
