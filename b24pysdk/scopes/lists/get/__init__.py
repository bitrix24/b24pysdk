from functools import cached_property
from typing import Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity
from .iblock import Iblock

__all__ = [
    "Get",
]


class Get(BaseEntity):
    """"""

    @cached_property
    def iblock(self) -> Iblock:
        """"""
        return Iblock(self)

    @type_checker
    def __call__(
            self,
            iblock_type_id: Text,
            *,
            iblock_id: Optional[int] = MISSING,
            iblock_code: Optional[Text] = MISSING,
            socnet_group_id: Optional[int] = MISSING,
            iblock_order: Optional[JSONDict] = MISSING,
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

        if socnet_group_id is not MISSING:
            params["SOCNET_GROUP_ID"] = socnet_group_id

        if iblock_order is not MISSING:
            params["IBLOCK_ORDER"] = iblock_order

        if start is not MISSING:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self,
            params=params,
            timeout=timeout,
        )
