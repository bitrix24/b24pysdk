from functools import cached_property
from typing import Annotated, Literal, Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest, BitrixAPIValueRequest
from ...schemas.results import CountResultData
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._adapters import BitrixResultAdapter
from .._base_scope import BaseScope
from .offline import Offline

__all__ = [
    "Event",
]


class Event(BaseScope):
    """"""

    @cached_property
    def offline(self) -> Offline:
        """"""
        return Offline(self)

    @type_checker
    def bind(
            self,
            event: Text,
            handler: Text,
            *,
            auth_type: Optional[int] = MISSING,
            event_type: Optional[Annotated[Text, Literal["offline", "online"]]] = MISSING,
            auth_connector: Optional[Text] = MISSING,
            options: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """"""

        params: JSONDict = {
            "event": event,
            "handler": handler,
        }

        if auth_type is not MISSING:
            params["auth_type"] = auth_type

        if event_type is not MISSING:
            params["event_type"] = event_type

        if auth_connector is not MISSING:
            params["auth_connector"] = auth_connector

        if options is not MISSING:
            params["options"] = options

        return self._make_bitrix_api_request(
            api_wrapper=self.bind,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            timeout=timeout,
        )

    @type_checker
    def unbind(
            self,
            event: Text,
            handler: Text,
            *,
            auth_type: Optional[int] = MISSING,
            event_type: Optional[Annotated[Text, Literal["offline", "online"]]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIValueRequest[CountResultData, int]:
        """"""

        params: JSONDict = {
            "event": event,
            "handler": handler,
        }

        if auth_type is not MISSING:
            params["auth_type"] = auth_type

        if event_type is not MISSING:
            params["event_type"] = event_type

        return self._make_bitrix_api_request(
            api_wrapper=self.unbind,
            params=params,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValueRequest,
            result_adapter=BitrixResultAdapter(int, wrapper="count"),
        )
