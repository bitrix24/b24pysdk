from typing import Iterable, Optional, Text, Union

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import B24Bool, JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Document",
]


class Document(BaseEntity):
    """"""

    @type_checker
    def add(
        self,
        template_id: int,
        *,
        value: Optional[Text] = None,
        values: Optional[JSONDict] = None,
        stamps_enabled: Optional[Union[bool, int]] = None,
        fields: Optional[JSONDict] = None,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "templateId": template_id,
        }

        if value is not None:
            params["value"] = value

        if values is not None:
            params["values"] = values

        if stamps_enabled is not None:
            params["stampsEnabled"] = B24Bool(stamps_enabled).to_b24()

        if fields is not None:
            params["fields"] = fields

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
        self,
        bitrix_id: int,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def enablepublicurl(
        self,
        bitrix_id: int,
        status: Union[bool, int],
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
            "status": B24Bool(status).to_b24(),
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.enablepublicurl,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
        self,
        bitrix_id: int,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def getfields(
        self,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        return self._make_bitrix_api_request(
            api_wrapper=self.getfields,
            timeout=timeout,
        )

    @type_checker
    def list(
        self,
        *,
        select: Optional[Iterable[Text]] = None,
        order: Optional[JSONDict] = None,
        filter: Optional[JSONDict] = None,
        start: Optional[int] = None,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {}

        if select is not None:
            if select.__class__ is not list:
                select = list(select)
            params["select"] = select

        if order is not None:
            params["order"] = order

        if filter is not None:
            params["filter"] = filter

        if start is not None:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
        self,
        bitrix_id: int,
        *,
        values: Optional[JSONDict] = None,
        stamps_enabled: Optional[Union[bool, int]] = None,
        fields: Optional[JSONDict] = None,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
        }

        if values is not None:
            params["values"] = values

        if stamps_enabled is not None:
            params["stampsEnabled"] = B24Bool(stamps_enabled).to_b24()

        if fields is not None:
            params["fields"] = fields

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
