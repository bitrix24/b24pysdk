from typing import Annotated, Literal, Text

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Status",
]


class Status(BaseEntity):
    """"""

    @type_checker
    def update(
            self,
            code: Text,
            message_id: int,
            status: Annotated[Text, Literal["delivered", "failed", "undelivered"]],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "CODE": code,
            "MESSAGE_ID": message_id,
            "STATUS": status,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
