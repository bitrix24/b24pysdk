from typing import Optional, Text, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Messages",
]


class Messages(BaseEntity):
    """"""

    @type_checker
    def get(
            self,
            dialog_id: Text,
            *,
            last_id: Optional[Union[int, Text]] = None,
            first_id: Optional[Union[int, Text]] = None,
            limit: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            DIALOG_ID=dialog_id,
        )

        if last_id is not None:
            params["LAST_ID"] = last_id

        if first_id is not None:
            params["FIRST_ID"] = first_id

        if limit is not None:
            params["LIMIT"] = limit

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )
