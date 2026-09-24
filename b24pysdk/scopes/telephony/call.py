from typing import Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONList, Number, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Call",
]


class Call(BaseEntity):
    """Class for managing call transcription attachments.

    Documentation: https://apidocs.bitrix24.com/api-reference/telephony/index.html
    """

    @type_checker
    def attach_transcription(
            self,
            call_id: Text,
            messages: JSONList,
            *,
            cost: Optional[Number] = MISSING,
            cost_currency: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add transcription to call

        Documentation: https://apidocs.bitrix24.com/api-reference/telephony/telephony-call-attach-transcription.html

        The method adds a transcription of the conversation to a completed call.

        Args:
            call_id: Call identifier;

            messages: Array of transcription utterances;

            cost: Cost of the transcription;

            cost_currency: Currency of the transcription cost;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "CALL_ID": call_id,
            "MESSAGES": messages,
        }

        if cost is not MISSING:
            params["COST"] = cost

        if cost_currency is not MISSING:
            params["COST_CURRENCY"] = cost_currency

        return self._make_bitrix_api_request(
            api_wrapper=self.attach_transcription,
            params=params,
            timeout=timeout,
        )
