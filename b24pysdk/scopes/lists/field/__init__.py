from functools import cached_property
from typing import Iterable, List, Optional, Text, Union

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest, BitrixAPIValueRequest, BitrixAPIValuesRequest
from ....constants.list import ListIBlockType
from ....objects.list.field._base_list_field import BaseListField
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._adapters import BitrixObjectAdapter, BitrixObjectsAdapter
from ..._base_entity import BaseEntity
from .type import Type

__all__ = [
    "Field",
]


class _ListFieldsAdapter(BitrixObjectsAdapter[BaseListField]):
    """Adapt values returned by lists.field.get to list-field objects."""

    def _unwrap_list_result(self, bitrix_result: JSONDict, /) -> List[JSONDict]:
        fields = list(bitrix_result.values())

        if not all(isinstance(field, dict) for field in fields):
            raise TypeError("Expected lists.field.get result values to be dictionaries.")

        return fields


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
            iblock_id: Optional[int] = MISSING,
            iblock_code: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIValueRequest[Text, BaseListField]:
        """"""

        params: JSONDict = {
            "IBLOCK_TYPE_ID": iblock_type_id,
            "FIELDS": fields,
        }

        if iblock_id is MISSING and iblock_code is MISSING:
            raise ValueError("Either 'iblock_id' or 'iblock_code' must be provided.")

        if iblock_id is not MISSING:
            params["IBLOCK_ID"] = iblock_id

        if iblock_code is not MISSING:
            params["IBLOCK_CODE"] = iblock_code

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValueRequest,
            result_adapter=BitrixObjectAdapter(
                "list.field",
                client=self._client,
                discriminator=(
                    ListIBlockType(iblock_type_id),
                    None if iblock_id is MISSING else iblock_id,
                ),
            ),
        )

    @type_checker
    def get(
            self,
            iblock_type_id: Text,
            *,
            iblock_id: Optional[int] = MISSING,
            iblock_code: Optional[Text] = MISSING,
            field_id: Union[Text, Iterable[Text]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIValuesRequest[JSONDict, BaseListField]:
        """"""

        params: JSONDict = {
            "IBLOCK_TYPE_ID": iblock_type_id,
        }

        if iblock_id is MISSING and iblock_code is MISSING:
            raise ValueError("Either 'iblock_id' or 'iblock_code' must be provided.")

        if iblock_id is not MISSING:
            params["IBLOCK_ID"] = iblock_id

        if iblock_code is not MISSING:
            params["IBLOCK_CODE"] = iblock_code

        if field_id is not MISSING:
            params["FIELD_ID"] = field_id if isinstance(field_id, str) else list(field_id)

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValuesRequest,
            result_adapter=_ListFieldsAdapter(
                "list.field",
                client=self._client,
                discriminator=(
                    ListIBlockType(iblock_type_id),
                    None if iblock_id is MISSING else iblock_id,
                ),
            ),
        )

    @type_checker
    def update(
            self,
            iblock_type_id: Text,
            field_id: Text,
            fields: JSONDict,
            *,
            iblock_id: Optional[int] = MISSING,
            iblock_code: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """"""

        params: JSONDict = {
            "IBLOCK_TYPE_ID": iblock_type_id,
            "FIELD_ID": field_id,
            "FIELDS": fields,
        }

        if iblock_id is MISSING and iblock_code is MISSING:
            raise ValueError("Either 'iblock_id' or 'iblock_code' must be provided.")

        if iblock_id is not MISSING:
            params["IBLOCK_ID"] = iblock_id

        if iblock_code is not MISSING:
            params["IBLOCK_CODE"] = iblock_code

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            iblock_type_id: Text,
            field_id: Text,
            *,
            iblock_id: Optional[int] = MISSING,
            iblock_code: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """"""

        params: JSONDict = {
            "IBLOCK_TYPE_ID": iblock_type_id,
            "FIELD_ID": field_id,
        }

        if iblock_id is MISSING and iblock_code is MISSING:
            raise ValueError("Either 'iblock_id' or 'iblock_code' must be provided.")

        if iblock_id is not MISSING:
            params["IBLOCK_ID"] = iblock_id

        if iblock_code is not MISSING:
            params["IBLOCK_CODE"] = iblock_code

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )
