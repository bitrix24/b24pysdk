from typing import Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.converters import bool_to_bitrix
from ....utils.functional import type_checker
from ....utils.types import JSONDict, JSONList, Timeout
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
        finalize: Optional[bool] = MISSING,
        status: Optional[JSONDict] = MISSING,
        properties: Optional[JSONList] = MISSING,
        overwrite_properties: Optional[bool] = MISSING,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "DELIVERY_ID": delivery_id,
            "REQUEST_ID": request_id,
        }

        if finalize is not MISSING:
            params["FINALIZE"] = bool_to_bitrix(finalize, is_required=True)

        if status is not MISSING:
            params["STATUS"] = status

        if properties is not MISSING:
            params["PROPERTIES"] = properties

        if overwrite_properties is not MISSING:
            params["OVERWRITE_PROPERTIES"] = bool_to_bitrix(overwrite_properties, is_required=True)

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
