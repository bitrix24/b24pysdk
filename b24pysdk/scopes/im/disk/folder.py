from typing import Optional, Text, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Folder",
]


class Folder(BaseEntity):
    """"""

    @type_checker
    def get(
            self,
            *,
            chat_id: Optional[Union[int, Text]] = None,
            dialog_id: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """"""

        params: JSONDict = {}

        if chat_id is not None:
            params["CHAT_ID"] = chat_id

        if dialog_id is not None:
            params["DIALOG_ID"] = dialog_id

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )
