from typing import Optional, Text, Union

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Personal",
]


class Personal(BaseEntity):
    """"""

    @type_checker
    def add(
            self,
            user_id: int,
            message: Text,
            *,
            message_out: Optional[Text] = MISSING,
            tag: Optional[Text] = MISSING,
            sub_tag: Optional[Text] = MISSING,
            attach: Optional[Union[JSONDict, Text]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[Union[int, bool]]:
        """"""

        params = {
            "USER_ID": user_id,
            "MESSAGE": message,
        }

        if message_out is not MISSING:
            params["MESSAGE_OUT"] = message_out

        if tag is not MISSING:
            params["TAG"] = tag

        if sub_tag is not MISSING:
            params["SUB_TAG"] = sub_tag

        if attach is not MISSING:
            params["ATTACH"] = attach

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )
