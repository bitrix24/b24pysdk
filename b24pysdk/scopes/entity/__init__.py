from functools import cached_property
from typing import Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_scope import BaseScope
from .item import Item
from .section import Section

__all__ = [
    "Entity",
]


class Entity(BaseScope):
    """"""

    @cached_property
    def section(self) -> Section:
        """"""
        return Section(self)

    @cached_property
    def item(self) -> Item:
        """"""
        return Item(self)

    @type_checker
    def add(
            self,
            entity: Text,
            name: Text,
            *,
            access: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "ENTITY": entity,
            "NAME": name,
        }

        if access is not None:
            params["ACCESS"] = access

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            entity: Text,
            *,
            name: Optional[Text] = None,
            access: Optional[JSONDict] = None,
            entity_new: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "ENTITY": entity,
        }

        if name is not None:
            params["NAME"] = name

        if access is not None:
            params["ACCESS"] = access

        if entity_new is not None:
            params["ENTITY_NEW"] = entity_new

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def rights(
            self,
            entity: Text,
            *,
            access: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "ENTITY": entity,
        }

        if access is not None:
            params["ACCESS"] = access

        return self._make_bitrix_api_request(
            api_wrapper=self.rights,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            *,
            entity: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if entity is not None:
            params["ENTITY"] = entity

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            entity: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "ENTITY": entity,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

