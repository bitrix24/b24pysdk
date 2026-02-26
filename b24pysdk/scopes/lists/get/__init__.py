from functools import cached_property
from typing import Optional, Text

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

    @type_checker
    def __call__(
            self,
            iblock_type_id: Text,
            *,
            iblock_id: Optional[int] = None,
            iblock_code: Optional[Text] = None,
            socnet_group_id: Optional[int] = None,
            iblock_order: Optional[JSONDict] = None,
            start: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "IBLOCK_TYPE_ID": iblock_type_id,
        }

        if iblock_id is not None:
            params["IBLOCK_ID"] = iblock_id

        if iblock_code is not None:
            params["IBLOCK_CODE"] = iblock_code

        if socnet_group_id is not None:
            params["SOCNET_GROUP_ID"] = socnet_group_id

        if iblock_order is not None:
            params["IBLOCK_ORDER"] = iblock_order

        if start is not None:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self,
            params=params,
            timeout=timeout,
        )

    @cached_property
    def iblock(self) -> Iblock:
        """"""
        return Iblock(self)
