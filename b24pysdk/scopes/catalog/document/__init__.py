from functools import cached_property
from typing import Iterable, Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity
from .element import Element
from .mode import Mode

__all__ = [
    "Document",
]


class Document(BaseEntity):
    """"""

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def cancel(
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
            api_wrapper=self.cancel,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def cancel_list(
            self,
            document_ids: Iterable[int],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if document_ids.__class__ is not list:
            document_ids = list(document_ids)

        params: JSONDict = {
            "documentIds": document_ids,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.cancel_list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def conduct(
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
            api_wrapper=self.conduct,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def conduct_list(
            self,
            document_ids: Iterable[int],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if document_ids.__class__ is not list:
            document_ids = list(document_ids)

        params: JSONDict = {
            "documentIds": document_ids,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.conduct_list,
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
    def delete_list(
            self,
            document_ids: Iterable[int],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if document_ids.__class__ is not list:
            document_ids = list(document_ids)

        params: JSONDict = {
            "documentIds": document_ids,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete_list,
            params=params,
            timeout=timeout,
        )

    @cached_property
    def element(self) -> Element:
        """"""
        return Element(self)

    @type_checker
    def get_fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        return self._make_bitrix_api_request(
            api_wrapper=self.get_fields,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            select: Optional[Iterable[Text]] = MISSING,
            filter: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {}

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        if filter is not MISSING:
            params["filter"] = filter

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @cached_property
    def mode(self) -> Mode:
        """"""
        return Mode(self)

    @type_checker
    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
