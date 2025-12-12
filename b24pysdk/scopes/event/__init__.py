from functools import cached_property
from typing import Annotated, Literal, Optional, Text

from ...bitrix_api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import Timeout
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
            auth_type: Optional[int] = None,
            event_type: Optional[Annotated[Text, Literal["offline", "online"]]] = None,
            auth_connector: Optional[Text] = None,
            options: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "event": event,
            "handler": handler,
        }

        if auth_type is not None:
            params["auth_type"] = auth_type

        if event_type is not None:
            params["event_type"] = event_type

        if auth_connector is not None:
            params["auth_connector"] = auth_connector

        if options is not None:
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
            auth_type: Optional[int] = None,
            event_type: Optional[Annotated[Text, Literal["offline", "online"]]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "event": event,
            "handler": handler,
        }

        if auth_type is not None:
            params["auth_type"] = auth_type

        if event_type is not None:
            params["event_type"] = event_type

        return self._make_bitrix_api_request(
            api_wrapper=self.unbind,
            params=params,
            timeout=timeout,
        )
