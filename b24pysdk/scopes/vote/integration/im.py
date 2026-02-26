from typing import Optional, Text

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Im",
]


class Im(BaseEntity):
    """"""

    @type_checker
    def send(
            self,
            chat_id: int,
            im_message_vote_data: JSONDict,
            *,
            template_id: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "chatId": chat_id,
            "IM_MESSAGE_VOTE_DATA": im_message_vote_data,
        }

        if template_id is not None:
            params["templateId"] = template_id

        return self._make_bitrix_api_request(
            api_wrapper=self.send,
            params=params,
            timeout=timeout,
        )
