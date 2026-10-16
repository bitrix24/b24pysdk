from typing import Text, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Message",
]


class Message(BaseEntity):
    """Class for sending messages in open channels.

    Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/messages/index.html
    """

    @type_checker
    def add(
            self,
            crm_entity_type: Text,
            crm_entity: Union[int, Text],
            user_id: Union[int, Text],
            chat_id: Union[int, Text],
            message: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Send a message to open channel

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/messages/imopenlines-crm-message-add.html

        The method sends a message on behalf of an employee or bot in a chat linked to a CRM entity.

        Args:
            crm_entity_type: Type of the CRM object;

            crm_entity: Identifier of the CRM object;

            user_id: Message sender identifier;

            chat_id: Identifier of the chat;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            CRM_ENTITY_TYPE=crm_entity_type,
            CRM_ENTITY=crm_entity,
            USER_ID=user_id,
            CHAT_ID=chat_id,
            MESSAGE=message,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )
