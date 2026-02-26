from typing import Optional, Text

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "System",
]


class System(BaseEntity):
    """"""

    @type_checker
    def add(
            self,
            user_id: int,
            message: Text,
            *,
            message_out: Optional[Text] = None,
            tag: Optional[Text] = None,
            sub_tag: Optional[Text] = None,
            attach: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "USER_ID": user_id,
            "MESSAGE": message,
        }

        if message_out is not None:
            params["MESSAGE_OUT"] = message_out

        if tag is not None:
            params["TAG"] = tag

        if sub_tag is not None:
            params["SUB_TAG"] = sub_tag

        if attach is not None:
            params["ATTACH"] = attach

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )
