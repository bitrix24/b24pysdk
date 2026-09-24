from functools import cached_property
from typing import Annotated, Iterable, Optional, Text

from ....._constants import MISSING
from .....api.requests import BitrixAPIValuesRequest
from .....constants.list import ListIBlockType, ListIBlockTypeLiteral
from .....objects.list.element._base_list_element import BaseListElement
from .....utils.functional import type_checker
from .....utils.types import JSONDict, JSONList, Timeout
from ...._adapters import BitrixObjectsAdapter
from ...._base_entity import BaseEntity
from .file import File

__all__ = [
    "Get",
]


class Get(BaseEntity):
    """Callable context for ``lists.element.get`` and nested methods."""

    @cached_property
    def file(self) -> File:
        """Return the list-element file helper context."""
        return File(self)

    @type_checker
    def __call__(
            self,
            iblock_type_id: Annotated[Text, ListIBlockTypeLiteral],
            *,
            iblock_id: Optional[int] = MISSING,
            iblock_code: Optional[Text] = MISSING,
            element_id: Optional[int] = MISSING,
            element_code: Optional[Text] = MISSING,
            select: Optional[Iterable[Text]] = MISSING,
            filter: Optional[JSONDict] = MISSING,
            start: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIValuesRequest[JSONList, BaseListElement]:
        """Return elements of the requested Bitrix24 list."""

        if iblock_id is MISSING and iblock_code is MISSING:
            raise ValueError("Pass iblock_id or iblock_code.")

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

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)

            params["SELECT"] = select

        if filter is not MISSING:
            params["FILTER"] = filter

        if start is not MISSING:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self,
            params=params,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValuesRequest,
            result_adapter=BitrixObjectsAdapter(
                BaseListElement.OBJECT_KEY,
                client=self._client,
                select=None if select is MISSING else select,
                discriminator=(
                    ListIBlockType(iblock_type_id),
                    None if iblock_id is MISSING else iblock_id,
                ),
            ),
        )
