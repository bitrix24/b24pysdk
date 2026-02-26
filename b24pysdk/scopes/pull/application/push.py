from typing import Iterable, Optional, Text

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Push",
]


class Push(BaseEntity):
    """"""

    @type_checker
    def add(
            self,
            user_id: Iterable[int],
            *,
            text: Optional[Text] = None,
            avatar: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if user_id.__class__ is not list:
            user_id = list(user_id)

        params = {
            "USER_ID": user_id,
        }

        if text is not None:
            params["TEXT"] = text

        if avatar is not None:
            params["AVATAR"] = avatar

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )
