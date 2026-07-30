from functools import cached_property
from typing import Iterable, Optional, Text

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity
from .file import File

__all__ = [
    "Get",
]


class Get(BaseEntity):
    """"""

    @cached_property
    def file(self) -> File:
        """"""
        return File(self)

    @type_checker
    def __call__(
            self,
            iblock_type_id: Text,
            *,
            iblock_id: Optional[int] = MISSING,
            iblock_code: Optional[Text] = MISSING,
            element_id: Optional[int] = MISSING,
            element_code: Optional[Text] = MISSING,
            select: Optional[Iterable[Text]] = MISSING,
            filter: Optional[JSONDict] = MISSING,
            element_order: Optional[JSONDict] = MISSING,
            start: Optional[int] = MISSING,
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

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)

            params["SELECT"] = select

        if filter is not MISSING:
            params["FILTER"] = filter

        if element_order is not MISSING:
            params["ELEMENT_ORDER"] = element_order

        if start is not MISSING:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self,
            params=params,
            timeout=timeout,
        )
