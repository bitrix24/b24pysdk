from typing import Annotated, Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....constants.list import ListIBlockTypeLiteral
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Type",
]


class Type(BaseEntity):
    """Methods for available Bitrix24 list field types.

    Documentation: https://apidocs.bitrix24.com/api-reference/lists/fields/index.html
    """

    @type_checker
    def get(
            self,
            iblock_type_id: Annotated[Text, ListIBlockTypeLiteral],
            *,
            iblock_id: Optional[int] = MISSING,
            iblock_code: Optional[Text] = MISSING,
            field_id: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """Get available field types for universal list

        Documentation: https://apidocs.bitrix24.com/api-reference/lists/fields/lists-field-type-get.html

        The method returns a list of available field types for the list.

        Args:
            iblock_type_id: Identifier of the information block type;

            iblock_id: Identifier of the information block;

            iblock_code: Symbolic code of the information block;

            field_id: Field identifier;

            timeout: Timeout in seconds.

        Return:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "IBLOCK_TYPE_ID": iblock_type_id,
        }

        if iblock_id is MISSING and iblock_code is MISSING:
            raise ValueError("Either 'iblock_id' or 'iblock_code' must be provided.")

        if iblock_id is not MISSING:
            params["IBLOCK_ID"] = iblock_id

        if iblock_code is not MISSING:
            params["IBLOCK_CODE"] = iblock_code

        if field_id is not MISSING:
            params["FIELD_ID"] = field_id

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )
