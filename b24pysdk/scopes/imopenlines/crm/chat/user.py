from typing import Optional, Text, Union

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "User",
]


class User(BaseEntity):
    """Class for managing users in an existing chats of the CRM objects.

    Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/chats/index.html
    """

    @type_checker
    def add(
            self,
            crm_entity_type: Text,
            crm_entity: Union[int, Text],
            user_id: Union[int, Text],
            *,
            chat_id: Optional[Union[int, Text]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add user to existing chat

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/chats/imopenlines-crm-chat-user-add.html

        The method adds to a chat associated with a CRM object.

        Args:
            crm_entity_type: Type of the CRM object;

            crm_entity: Identifier of the CRM object;

            user_id: Identifier of the user or bot to be added to the chat;

            chat_id: Identifier of the chat;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            CRM_ENTITY_TYPE=crm_entity_type,
            CRM_ENTITY=crm_entity,
            USER_ID=user_id,
        )

        if chat_id is not MISSING:
            params["CHAT_ID"] = chat_id

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            crm_entity_type: Text,
            crm_entity: Union[int, Text],
            user_id: Union[int, Text],
            *,
            chat_id: Optional[Union[int, Text]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Remove user from chat

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/chats/imopenlines-crm-chat-user-delete.html

        The method removes a user from the chat associated with the CRM object.

        Args:
            crm_entity_type: Type of the CRM object;

            crm_entity: Identifier of the CRM object;

            user_id: Identifier of the user or bot;

            chat_id: Identifier of the chat;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            CRM_ENTITY_TYPE=crm_entity_type,
            CRM_ENTITY=crm_entity,
            USER_ID=user_id,
        )

        if chat_id is not MISSING:
            params["CHAT_ID"] = chat_id

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )
