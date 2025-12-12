from typing import Iterable, Optional, Text

from ...bitrix_api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Offline",
]


class Offline(BaseEntity):
    """"""

    @type_checker
    def get(
            self,
            *,
            filter: Optional[JSONDict] = None,
            order: Optional[JSONDict] = None,
            limit: Optional[int] = None,
            clear: Optional[bool] = None,
            process_id: Optional[Text] = None,
            auth_connector: Optional[Text] = None,
            error: Optional[bool] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if filter is not None:
            params["filter"] = filter

        if order is not None:
            params["order"] = order

        if limit is not None:
            params["limit"] = limit

        if clear is not None:
            params["clear"] = int(clear)

        if process_id is not None:
            params["process_id"] = process_id

        if auth_connector is not None:
            params["auth_connector"] = auth_connector

        if error is not None:
            params["error"] = int(error)

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            filter: Optional[JSONDict] = None,
            order: Optional[JSONDict] = None,
            start: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if filter is not None:
            params["filter"] = filter

        if order is not None:
            params["order"] = order

        if start is not None:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def clear(
            self,
            process_id: Text,
            *,
            bitrix_id: Optional[Iterable[int]] = None,
            message_id: Optional[Iterable[int]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "process_id": process_id,
        }

        if bitrix_id is not None:
            if bitrix_id.__class__ is not list:
                bitrix_id = list(bitrix_id)

            params["id"] = bitrix_id

        if message_id is not None:
            if message_id.__class__ is not list:
                message_id = list(message_id)

            params["message_id"] = message_id

        return self._make_bitrix_api_request(
            api_wrapper=self.clear,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def error(
            self,
            process_id: Text,
            *,
            message_id: Optional[Iterable[int]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "process_id": process_id,
        }

        if message_id is not None:
            if message_id.__class__ is not list:
                message_id = list(message_id)

            params["message_id"] = message_id

        return self._make_bitrix_api_request(
            api_wrapper=self.error,
            params=params,
            timeout=timeout,
        )
