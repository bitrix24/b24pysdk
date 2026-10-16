from functools import cached_property
from typing import Optional, Text, Union

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.converters import bool_to_bitrix
from .....utils.functional import type_checker
from .....utils.types import Timeout
from ...._base_entity import BaseEntity
from .user import User

__all__ = [
    "Chat",
]


class Chat(BaseEntity):
    """Class for managing CRM object chats.

    Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/chats/index.html
    """

    @cached_property
    def user(self) -> User:
        """"""
        return User(self)

    @type_checker
    def get(
            self,
            crm_entity_type: Text,
            crm_entity: Union[int, Text],
            *,
            active_only: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get chats for CRM object

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/chats/imopenlines-crm-chat-get.html

        The method retrieves a list of chats associated with a CRM object.

        Args:
            crm_entity_type: Type of the CRM object;

            crm_entity: Identifier of the CRM object;

            active_only: Flag to return only active chats;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            CRM_ENTITY_TYPE=crm_entity_type,
            CRM_ENTITY=crm_entity,
        )

        if active_only is not MISSING:
            params["ACTIVE_ONLY"] = bool_to_bitrix(active_only, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_last_id(
            self,
            crm_entity_type: Text,
            crm_entity: Union[int, Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the identifier of the last chat

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/chats/imopenlines-crm-chat-get-last-id.html

        The method retrieves the identifier of the last chat associated with the CRM object.

        Args:
            crm_entity_type: Type of the CRM object;

            crm_entity: Identifier of the CRM object;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            CRM_ENTITY_TYPE=crm_entity_type,
            CRM_ENTITY=crm_entity,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.get_last_id,
            params=params,
            timeout=timeout,
        )
