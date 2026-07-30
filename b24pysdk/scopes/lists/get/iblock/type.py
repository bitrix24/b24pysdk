from typing import Optional, Text

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
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
            iblock_id: Optional[int] = MISSING,
            iblock_code: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {}

        if iblock_id is MISSING and iblock_code is MISSING:
            raise ValueError("Either 'iblock_id' or 'iblock_code' must be provided.")

        if iblock_id is not MISSING:
            params["IBLOCK_ID"] = iblock_id

        if iblock_code is not MISSING:
            params["IBLOCK_CODE"] = iblock_code

        return self._make_bitrix_api_request(
            api_wrapper=self.id,
            params=params,
            timeout=timeout,
        )
