from typing import Text, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Read",
]


class Read(BaseEntity):
    """"""

    @type_checker
    def __call__(
            self,
            dialog_id: Text,
            message_id: Union[int, Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[Union[JSONDict, bool]]:
        """"""

        params = dict(
            DIALOG_ID=dialog_id,
            MESSAGE_ID=message_id,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def all(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """"""

        return self._make_bitrix_api_request(
            api_wrapper=self.all,
            timeout=timeout,
        )
