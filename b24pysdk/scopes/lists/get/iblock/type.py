from typing import Optional, Text

from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "Type",
]


class Type(BaseEntity):
    """"""

    @type_checker
    def id(
            self,
            *,
            iblock_id: Optional[int] = None,
            iblock_code: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if iblock_id is not None:
            params["IBLOCK_ID"] = iblock_id

        if iblock_code is not None:
            params["IBLOCK_CODE"] = iblock_code

        return self._make_bitrix_api_request(
            api_wrapper=self.id,
            params=params or None,
            timeout=timeout,
        )
