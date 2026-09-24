from typing import Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import classproperty, type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Im",
]


class Im(BaseEntity):
    """Class for poll creation.

    Documentation: https://apidocs.bitrix24.com/api-reference/vote/index.html
    """

    @classproperty
    def _name(cls):
        return "Im"

    @type_checker
    def send(
            self,
            chat_id: int,
            im_message_vote_data: JSONDict,
            *,
            template_id: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create and send a vote in chat

        Documentation: https://apidocs.bitrix24.com/api-reference/vote/vote.integration.im.send.html

        The method creates and sends a vote to the specified chat in the messanger.

        Args:
            chat_id: Cha identifier;

            im_message_vote_data: Vote data containing the question and answer options;

            template_id: A unique identifier for the request, with no format requirements;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "chatId": chat_id,
            "IM_MESSAGE_VOTE_DATA": im_message_vote_data,
        }

        if template_id is not MISSING:
            params["templateId"] = template_id

        return self._make_bitrix_api_request(
            api_wrapper=self.send,
            params=params,
            timeout=timeout,
        )
