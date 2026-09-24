from functools import cached_property
from typing import Annotated, Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest, BitrixAPIValueRequest
from ...constants.list import ListIBlockTypeLiteral
from ...objects.list._base_list import BaseList
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._adapters import BitrixObjectAdapter
from .._base_scope import BaseScope
from .element import Element
from .field import Field
from .get import Get
from .section import Section

__all__ = [
    "Lists",
]


class Lists(BaseScope):
    """Methods for Bitrix24 universal lists."""

    @cached_property
    def element(self) -> Element:
        """Return the list-element context."""
        return Element(self)

    @cached_property
    def field(self) -> Field:
        """Return the list-field context."""
        return Field(self)

    @cached_property
    def get(self) -> Get:
        """Return the callable list retrieval context."""
        return Get(self)

    @cached_property
    def section(self) -> Section:
        """Return the list-section context."""
        return Section(self)

    @type_checker
    def add(
            self,
            iblock_type_id: Annotated[Text, ListIBlockTypeLiteral],
            iblock_code: Text,
            fields: JSONDict,
            *,
            socnet_group_id: Optional[int] = MISSING,
            messages: Optional[JSONDict] = MISSING,
            rights: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIValueRequest[int, BaseList]:
        """Create a universal list and adapt its identifier to a list object."""

        params: JSONDict = {
            "IBLOCK_TYPE_ID": iblock_type_id,
            "IBLOCK_CODE": iblock_code,
            "FIELDS": fields,
        }

        if socnet_group_id is not MISSING:
            params["SOCNET_GROUP_ID"] = socnet_group_id

        if messages is not MISSING:
            params["MESSAGES"] = messages

        if rights is not MISSING:
            params["RIGHTS"] = rights

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValueRequest,
            result_adapter=BitrixObjectAdapter(
                BaseList.OBJECT_KEY,
                client=self._client,
                discriminator=iblock_type_id,
            ),
        )

    @type_checker
    def delete(
            self,
            iblock_type_id: Annotated[Text, ListIBlockTypeLiteral],
            *,
            iblock_id: Optional[int] = MISSING,
            iblock_code: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Delete a universal list by identifier or symbolic code."""

        params: JSONDict = {
            "IBLOCK_TYPE_ID": iblock_type_id,
        }

        if iblock_id is not MISSING:
            params["IBLOCK_ID"] = iblock_id

        if iblock_code is not MISSING:
            params["IBLOCK_CODE"] = iblock_code

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            iblock_type_id: Annotated[Text, ListIBlockTypeLiteral],
            fields: JSONDict,
            *,
            iblock_id: Optional[int] = MISSING,
            iblock_code: Optional[Text] = MISSING,
            socnet_group_id: Optional[int] = MISSING,
            messages: Optional[JSONDict] = MISSING,
            rights: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Update a universal list by identifier or symbolic code."""

        params: JSONDict = {
            "IBLOCK_TYPE_ID": iblock_type_id,
            "FIELDS": fields,
        }

        if iblock_id is not MISSING:
            params["IBLOCK_ID"] = iblock_id

        if iblock_code is not MISSING:
            params["IBLOCK_CODE"] = iblock_code

        if socnet_group_id is not MISSING:
            params["SOCNET_GROUP_ID"] = socnet_group_id

        if messages is not MISSING:
            params["MESSAGES"] = messages

        if rights is not MISSING:
            params["RIGHTS"] = rights

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
