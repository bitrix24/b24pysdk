from typing import Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONList, Number, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Call",
]


class Call(BaseEntity):
    """"""

    @type_checker
    def attach_transcription(
            self,
            call_id: Text,
            messages: JSONList,
            *,
            cost: Optional[Number] = None,
            cost_currency: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "CALL_ID": call_id,
            "MESSAGES": messages,
        }

        if cost is not None:
            params["COST"] = cost

        if cost_currency is not None:
            params["COST_CURRENCY"] = cost_currency

        return self._make_bitrix_api_request(
            api_wrapper=self.attach_transcription,
            params=params,
            timeout=timeout,
        )
