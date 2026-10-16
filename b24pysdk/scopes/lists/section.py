from typing import Annotated, Iterable, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest, BitrixAPIValueRequest, BitrixAPIValuesRequest
from ...constants.list import ListIBlockType, ListIBlockTypeLiteral
from ...objects.list.section import BaseListSection
from ...utils.functional import type_checker
from ...utils.types import JSONDict, JSONList, Timeout
from .._adapters import BitrixObjectAdapter, BitrixObjectsAdapter
from .._base_entity import BaseEntity

__all__ = [
    "Section",
]


class Section(BaseEntity):
    """Methods for Bitrix24 universal-list sections.

    Documentation: http://apidocs.bitrix24.com/api-reference/lists/sections/index.html
    """

    @type_checker
    def add(
            self,
            iblock_type_id: Annotated[Text, ListIBlockTypeLiteral],
            section_code: Text,
            fields: JSONDict,
            *,
            iblock_id: int = MISSING,
            iblock_code: Text = MISSING,
            iblock_section_id: int = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIValueRequest[int, BaseListSection]:
        """Create a section of the universal list

        Documentation: https://apidocs.bitrix24.com/api-reference/lists/sections/lists-section-add.html

        The method creates a list section.

        Args:
            iblock_type_id: Identifier of the information block type;

            section_code: Symbolic code of the section;

            fields: Array of fields;

            iblock_id: Identifier of the information block;

            iblock_code: Symbolic code of the information block;

            iblock_section_id: Identifier of the parent section;

            timeout: Timeout in seconds.

        Return:
            Instance of BitrixAPIValueRequest
        """

        if iblock_id is MISSING and iblock_code is MISSING:
            raise ValueError("Pass iblock_id or iblock_code.")

        params: JSONDict = {
            "IBLOCK_TYPE_ID": iblock_type_id,
            "SECTION_CODE": section_code,
            "FIELDS": fields,
        }

        if iblock_id is not MISSING:
            params["IBLOCK_ID"] = iblock_id

        if iblock_code is not MISSING:
            params["IBLOCK_CODE"] = iblock_code

        if iblock_section_id is not MISSING:
            params["IBLOCK_SECTION_ID"] = iblock_section_id

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValueRequest,
            result_adapter=BitrixObjectAdapter(
                "list.section",
                client=self._client,
                discriminator=(
                    ListIBlockType(iblock_type_id),
                    None if iblock_id is MISSING else iblock_id,
                ),
            ),
        )

    @type_checker
    def get(
            self,
            iblock_type_id: Annotated[Text, ListIBlockTypeLiteral],
            *,
            iblock_id: int = MISSING,
            iblock_code: Text = MISSING,
            filter: JSONDict = MISSING,
            select: Iterable[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIValuesRequest[JSONList, BaseListSection]:
        """Get section parameters or list of sections

        Documentation: https://apidocs.bitrix24.com/api-reference/lists/sections/lists-section-get.html

        THe method returns a section or a list of sections.

        Args:
            iblock_type_id: Identifier of the information block type;

            iblock_id: Identifier of the information block;

            iblock_code: Symbolic code of the information block;

            filter: Object for filtering;

            select: Array with fields to select;

            timeout: Timeout in seconds.

        Return:
            Instance of BitrixAPIValueRequest
        """

        if iblock_id is MISSING and iblock_code is MISSING:
            raise ValueError("Pass iblock_id or iblock_code.")

        params: JSONDict = {
            "IBLOCK_TYPE_ID": iblock_type_id,
        }

        if iblock_id is not MISSING:
            params["IBLOCK_ID"] = iblock_id

        if iblock_code is not MISSING:
            params["IBLOCK_CODE"] = iblock_code

        if filter is not MISSING:
            params["FILTER"] = filter

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)

            params["SELECT"] = select

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValuesRequest,
            result_adapter=BitrixObjectsAdapter(
                "list.section",
                client=self._client,
                select=None if select is MISSING else select,
                discriminator=(
                    ListIBlockType(iblock_type_id),
                    None if iblock_id is MISSING else iblock_id,
                ),
            ),
        )

    @type_checker
    def update(
            self,
            iblock_type_id: Annotated[Text, ListIBlockTypeLiteral],
            fields: JSONDict,
            *,
            iblock_id: int = MISSING,
            iblock_code: Text = MISSING,
            section_id: int = MISSING,
            section_code: Text = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Update the section of the universal list

        Documentation: https://apidocs.bitrix24.com/api-reference/lists/sections/lists-section-update.html

        The method updates a list section.

        Args:
            iblock_type_id: Identifier of the information block type;

            fields: Array of fields;

            iblock_id: Identifier of the information block;

            iblock_code: Symbolic code of the information block;

            section_id: Identifier of the section;

            section_code: Symbolic code of the section;

            timeout: Timeout in seconds.

        Return:
            Instance of BitrixAPIRequest
        """

        if iblock_id is MISSING and iblock_code is MISSING:
            raise ValueError("Pass iblock_id or iblock_code.")

        if section_id is MISSING and section_code is MISSING:
            raise ValueError("Pass section_id or section_code.")

        params: JSONDict = {
            "IBLOCK_TYPE_ID": iblock_type_id,
            "FIELDS": fields,
        }

        if iblock_id is not MISSING:
            params["IBLOCK_ID"] = iblock_id

        if iblock_code is not MISSING:
            params["IBLOCK_CODE"] = iblock_code

        if section_id is not MISSING:
            params["SECTION_ID"] = section_id

        if section_code is not MISSING:
            params["SECTION_CODE"] = section_code

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            iblock_type_id: Annotated[Text, ListIBlockTypeLiteral],
            *,
            iblock_id: int = MISSING,
            iblock_code: Text = MISSING,
            section_id: int = MISSING,
            section_code: Text = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Delete the section of the universal list

        Documentation: https://apidocs.bitrix24.com/api-reference/lists/sections/lists-section-delete.html

        The method removes a section from the list.

        Args:
            iblock_type_id: Identifier of the information block type;

            iblock_id: Identifier of the information block;

            iblock_code: Symbolic code of the information block;

            section_id: Identifier of the section;

            section_code: Symbolic code of the section;

            timeout: Timeout in seconds.

        Return:
            Instance of BitrixAPIRequest
        """

        if iblock_id is MISSING and iblock_code is MISSING:
            raise ValueError("Pass iblock_id or iblock_code.")

        if section_id is MISSING and section_code is MISSING:
            raise ValueError("Pass section_id or section_code.")

        params: JSONDict = {
            "IBLOCK_TYPE_ID": iblock_type_id,
        }

        if iblock_id is not MISSING:
            params["IBLOCK_ID"] = iblock_id

        if iblock_code is not MISSING:
            params["IBLOCK_CODE"] = iblock_code

        if section_id is not MISSING:
            params["SECTION_ID"] = section_id

        if section_code is not MISSING:
            params["SECTION_CODE"] = section_code

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )
