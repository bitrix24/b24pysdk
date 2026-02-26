from typing import Optional, Text, Union

from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "User",
]


class User(BaseEntity):
    """"""

    @type_checker
    def add(
            self,
            crm_entity_type: Text,
            crm_entity: Union[int, Text],
            user_id: Union[int, Text],
            *,
            chat_id: Optional[Union[int, Text]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            CRM_ENTITY_TYPE=crm_entity_type,
            CRM_ENTITY=crm_entity,
            USER_ID=user_id,
        )

        if chat_id is not None:
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
            chat_id: Optional[Union[int, Text]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            CRM_ENTITY_TYPE=crm_entity_type,
            CRM_ENTITY=crm_entity,
            USER_ID=user_id,
        )

        if chat_id is not None:
            params["CHAT_ID"] = chat_id

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )
