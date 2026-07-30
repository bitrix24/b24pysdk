from typing import Optional, Text, Union

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Name",
]


class Name(BaseEntity):
    """"""

    @type_checker
    def set(
            self,
            connector: Text,
            line: Union[int, Text],
            chat_id: Text,
            name: Text,
            *,
            user_id: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            CONNECTOR=connector,
            LINE=line,
            CHAT_ID=chat_id,
            NAME=name,
        )

        if user_id is not MISSING:
            params["USER_ID"] = user_id

        return self._make_bitrix_api_request(
            api_wrapper=self.set,
            params=params,
            timeout=timeout,
        )
