from typing import Iterable, Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Section",
]


class Section(BaseEntity):
    """"""

    @type_checker
    def add(
            self,
            iblock_type_id: Text,
            section_code: Text,
            fields: JSONDict,
            *,
            iblock_id: Optional[int] = MISSING,
            iblock_code: Optional[Text] = MISSING,
            iblock_section_id: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

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
        )

    @type_checker
    def delete(
            self,
            iblock_type_id: Text,
            *,
            iblock_id: Optional[int] = MISSING,
            iblock_code: Optional[Text] = MISSING,
            section_id: Optional[int] = MISSING,
            section_code: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

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

    @type_checker
    def get(
            self,
            iblock_type_id: Text,
            *,
            iblock_id: Optional[int] = MISSING,
            iblock_code: Optional[Text] = MISSING,
            filter: Optional[JSONDict] = MISSING,
            select: Optional[Iterable[Text]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

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
        )

    @type_checker
    def update(
            self,
            iblock_type_id: Text,
            fields: JSONDict,
            *,
            iblock_id: Optional[int] = MISSING,
            iblock_code: Optional[Text] = MISSING,
            section_id: Optional[int] = MISSING,
            section_code: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

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
