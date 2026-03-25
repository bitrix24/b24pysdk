from functools import cached_property
from typing import Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_scope import BaseScope
from .element import Element
from .field import Field
from .get import Get
from .section import Section

__all__ = [
    "Lists",
]


class Lists(BaseScope):
    """"""

    @cached_property
    def element(self) -> Element:
        """"""
        return Element(self)

    @cached_property
    def field(self) -> Field:
        """"""
        return Field(self)

    @cached_property
    def get(self) -> Get:
        """"""
        return Get(self)

    @cached_property
    def section(self) -> Section:
        """"""
        return Section(self)

    @type_checker
    def add(
            self,
            iblock_type_id: Text,
            iblock_code: Text,
            fields: JSONDict,
            *,
            socnet_group_id: Optional[int] = None,
            messages: Optional[JSONDict] = None,
            rights: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "IBLOCK_TYPE_ID": iblock_type_id,
            "IBLOCK_CODE": iblock_code,
            "FIELDS": fields,
        }

        if socnet_group_id is not None:
            params["SOCNET_GROUP_ID"] = socnet_group_id

        if messages is not None:
            params["MESSAGES"] = messages

        if rights is not None:
            params["RIGHTS"] = rights

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
            iblock_id: Optional[int] = None,
            iblock_code: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "IBLOCK_TYPE_ID": iblock_type_id,
        }

        if iblock_id is not None:
            params["IBLOCK_ID"] = iblock_id

        if iblock_code is not None:
            params["IBLOCK_CODE"] = iblock_code

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
            iblock_id: Optional[int] = None,
            iblock_code: Optional[Text] = None,
            socnet_group_id: Optional[int] = None,
            messages: Optional[JSONDict] = None,
            rights: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "IBLOCK_TYPE_ID": iblock_type_id,
            "FIELDS": fields,
        }

        if iblock_id is not None:
            params["IBLOCK_ID"] = iblock_id

        if iblock_code is not None:
            params["IBLOCK_CODE"] = iblock_code

        if socnet_group_id is not None:
            params["SOCNET_GROUP_ID"] = socnet_group_id

        if messages is not None:
            params["MESSAGES"] = messages

        if rights is not None:
            params["RIGHTS"] = rights

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
