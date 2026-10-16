from typing import Optional, Text

from ....._constants import MISSING
from .....api.requests import BitrixAPIValueRequest
from .....constants.list import ListIBlockType, ListIBlockTypeLiteral
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._adapters import BitrixResultAdapter
from ...._base_entity import BaseEntity

__all__ = [
    "Type",
]


class Type(BaseEntity):
    """Class for retrieving identifier of the information block type.

    Documentation: https://apidocs.bitrix24.com/api-reference/lists/lists/index.html
    """

    @type_checker
    def id(
            self,
            *,
            iblock_id: Optional[int] = MISSING,
            iblock_code: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIValueRequest[ListIBlockTypeLiteral, ListIBlockType]:
        """Get the information block type ID

        Documentation: https://apidocs.bitrix24.com/api-reference/lists/lists/lists-get-iblock-type-id.html

        The method returns the unformation block type ID.

        Args:
            iblock_id: Information block ID;

            iblock_code: Symbolic code of the information block;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

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
            bitrix_api_request_type=BitrixAPIValueRequest,
            result_adapter=BitrixResultAdapter(ListIBlockType),
        )
