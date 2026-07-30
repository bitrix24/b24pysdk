from functools import cached_property
from typing import Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity
from .get import Get

__all__ = [
    "Element",
]


class Element(BaseEntity):
    """"""

    @cached_property
    def get(self) -> Get:
        """"""
        return Get(self)


    @type_checker
    def add(
            self,
            iblock_type_id: Text,
            element_code: Text,
            fields: JSONDict,
            *,
            iblock_id: Optional[int] = MISSING,
            iblock_code: Optional[Text] = MISSING,
            iblock_section_id: Optional[int] = MISSING,
            list_element_url: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "IBLOCK_TYPE_ID": iblock_type_id,
            "ELEMENT_CODE": element_code,
            "FIELDS": fields,
        }

        if iblock_id is not MISSING:
            params["IBLOCK_ID"] = iblock_id

        if iblock_code is not MISSING:
            params["IBLOCK_CODE"] = iblock_code

        if iblock_section_id is not MISSING:
            params["IBLOCK_SECTION_ID"] = iblock_section_id

        if list_element_url is not MISSING:
            params["LIST_ELEMENT_URL"] = list_element_url

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
            element_id: Optional[int] = MISSING,
            element_code: Optional[Text] = MISSING,
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

        if element_id is not MISSING:
            params["ELEMENT_ID"] = element_id

        if element_code is not MISSING:
            params["ELEMENT_CODE"] = element_code

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
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
            element_id: Optional[int] = MISSING,
            element_code: Optional[Text] = MISSING,
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

        if element_id is not MISSING:
            params["ELEMENT_ID"] = element_id

        if element_code is not MISSING:
            params["ELEMENT_CODE"] = element_code

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
