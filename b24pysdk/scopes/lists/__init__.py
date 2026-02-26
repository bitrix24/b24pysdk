from functools import cached_property
from typing import Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_scope import BaseScope
from .get import Get

__all__ = [
    "Lists",
]


class Lists(BaseScope):
    """"""

    @type_checker
    def add(
            self,
            iblock_type_id: Text,
            iblock_code: Text,
            *,
            socnet_group_id: Optional[int] = None,
            fields: Optional[JSONDict] = None,
            messages: Optional[JSONDict] = None,
            rights: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "IBLOCK_TYPE_ID": iblock_type_id,
            "IBLOCK_CODE": iblock_code,
        }

        if socnet_group_id is not None:
            params["SOCNET_GROUP_ID"] = socnet_group_id

        if fields is not None:
            params["FIELDS"] = fields

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
            socnet_group_id: Optional[int] = None,
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

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @cached_property
    def get(self) -> Get:
        """"""
        return Get(self)

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

        params = {
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
