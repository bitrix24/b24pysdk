from functools import cached_property
from typing import Optional, Text

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity
from .type import Type

__all__ = [
    "Field",
]


class Field(BaseEntity):
    """"""

    @cached_property
    def type(self) -> Type:
        """"""
        return Type(self)

    @type_checker
    def add(
            self,
            iblock_type_id: Text,
            fields: JSONDict,
            *,
            iblock_id: Optional[int] = None,
            iblock_code: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "IBLOCK_TYPE_ID": iblock_type_id,
            "FIELDS": fields,
        }

        if iblock_id is None and iblock_code is None:
            raise ValueError("Either 'iblock_id' or 'iblock_code' must be provided.")

        if iblock_id is not None:
            params["IBLOCK_ID"] = iblock_id

        if iblock_code is not None:
            params["IBLOCK_CODE"] = iblock_code

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            iblock_type_id: Text,
            field_id: Text,
            *,
            iblock_id: Optional[int] = None,
            iblock_code: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "IBLOCK_TYPE_ID": iblock_type_id,
            "FIELD_ID": field_id,
        }

        if iblock_id is None and iblock_code is None:
            raise ValueError("Either 'iblock_id' or 'iblock_code' must be provided.")

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
    def get(
            self,
            iblock_type_id: Text,
            *,
            iblock_id: Optional[int] = None,
            iblock_code: Optional[Text] = None,
            field_id: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "IBLOCK_TYPE_ID": iblock_type_id,
        }

        if iblock_id is None and iblock_code is None:
            raise ValueError("Either 'iblock_id' or 'iblock_code' must be provided.")

        if iblock_id is not None:
            params["IBLOCK_ID"] = iblock_id

        if iblock_code is not None:
            params["IBLOCK_CODE"] = iblock_code

        if field_id is not None:
            params["FIELD_ID"] = field_id

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            iblock_type_id: Text,
            field_id: Text,
            fields: JSONDict,
            *,
            iblock_id: Optional[int] = None,
            iblock_code: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "IBLOCK_TYPE_ID": iblock_type_id,
            "FIELD_ID": field_id,
            "FIELDS": fields,
        }

        if iblock_id is None and iblock_code is None:
            raise ValueError("Either 'iblock_id' or 'iblock_code' must be provided.")

        if iblock_id is not None:
            params["IBLOCK_ID"] = iblock_id

        if iblock_code is not None:
            params["IBLOCK_CODE"] = iblock_code

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
