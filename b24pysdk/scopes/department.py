from typing import TYPE_CHECKING, Optional, Text

from ..bitrix_api.classes import BitrixAPIRequest
from ..utils.functional import type_checker
from ..utils.types import Timeout
from .scope import Scope

if TYPE_CHECKING:
    from .. import Client

__all__ = [
    "Department",
]


class Department(Scope):
    """"""

    def __init__(self, client: "Client"):
        super().__init__(client)

    @type_checker
    def fields(
            self,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._make_bitrix_api_request(
            api_method=self.fields,
            timeout=timeout,
        )

    @type_checker
    def add(
            self,
            name: Text,
            parent: int,
            sort: Optional[int] = None,
            uf_head: Optional[int] = None,
            timeout: Optional[Timeout] = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "NAME": name,
            "PARENT": parent,
        }

        if sort is not None:
            params["SORT"] = sort

        if uf_head is not None:
            params["UF_HEAD"] = uf_head

        return self._make_bitrix_api_request(
            api_method=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            sort: Optional[Text] = None,
            order: Optional[Text] = None,
            bitrix_id: Optional[int] = None,
            name: Optional[Text] = None,
            parent: Optional[int] = None,
            uf_head: Optional[int] = None,
            start: Optional[int] = None,
            timeout: Optional[Timeout] = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if sort is not None:
            params["sort"] = sort

        if order is not None:
            params["order"] = order

        if bitrix_id is not None:
            params["ID"] = bitrix_id

        if name is not None:
            params["NAME"] = name

        if parent is not None:
            params["PARENT"] = parent

        if uf_head is not None:
            params["UF_HEAD"] = uf_head

        if start is not None:
            params["START"] = start

        return self._make_bitrix_api_request(
            api_method=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            bitrix_id: int,
            name: Optional[Text] = None,
            sort: Optional[int] = None,
            parent: Optional[int] = None,
            uf_head: Optional[int] = None,
            timeout: Optional[Timeout] = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "ID": bitrix_id,
        }

        if name is not None:
            params["NAME"] = name

        if sort is not None:
            params["SORT"] = sort

        if parent is not None:
            params["PARENT"] = parent

        if uf_head is not None:
            params["UF_HEAD"] = uf_head

        return self._make_bitrix_api_request(
            api_method=self.update,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            timeout: Optional[Timeout] = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "ID": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_method=self.delete,
            params=params,
            timeout=timeout,
        )
