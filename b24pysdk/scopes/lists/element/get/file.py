from typing import Optional, Text

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "File",
]


class File(BaseEntity):
    """"""

    @type_checker
    def url(
            self,
            iblock_type_id: Text,
            field_id: int,
            *,
            iblock_id: Optional[int] = MISSING,
            iblock_code: Optional[Text] = MISSING,
            element_id: Optional[int] = MISSING,
            element_code: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "IBLOCK_TYPE_ID": iblock_type_id,
            "FIELD_ID": field_id,
        }

        if iblock_id is not MISSING:
            params["IBLOCK_ID"] = iblock_id

        if iblock_code is not MISSING:
            params["IBLOCK_CODE"] = iblock_code

        if element_id is not MISSING:
            params["ELEMENT_ID"] = element_id

        if element_code is not MISSING:
            params["ELEMENT_CODE"] = element_code

        return self._make_bitrix_api_request(
            api_wrapper=self.url,
            params=params,
            timeout=timeout,
        )
