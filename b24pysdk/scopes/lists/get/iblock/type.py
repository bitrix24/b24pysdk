from typing import Text

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
            iblock_id: int,
            iblock_code: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "IBLOCK_ID": iblock_id,
            "IBLOCK_CODE": iblock_code,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.id,
            params=params or None,
            timeout=timeout,
        )
