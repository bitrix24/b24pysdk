from typing import Optional, Text

from ...bitrix_api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Event",
]


class Event(BaseEntity):
    """"""

    @type_checker
    def send(
            self,
            event_token: Text,
            return_values: JSONDict,
            *,
            log_message: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "EVENT_TOKEN": event_token,
            "RETURN_VALUES": return_values,
        }

        if log_message is not None:
            params["LOG_MESSAGE"] = log_message

        return self._make_bitrix_api_request(
            api_wrapper=self.send,
            params=params,
            timeout=timeout,
        )
