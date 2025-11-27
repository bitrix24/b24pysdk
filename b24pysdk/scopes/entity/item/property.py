from typing import Optional, Text

from ....bitrix_api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Property",
]


class Property(BaseEntity):
    """"""

    @type_checker
    def get(
            self,
            entity: Text,
            *,
            property_code: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "ENTITY": entity,
        }

        if property_code is not None:
            params["PROPERTY"] = property_code

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def add(
            self,
            entity: Text,
            property_code: Text,
            name: Text,
            type_: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "ENTITY": entity,
            "PROPERTY": property_code,
            "NAME": name,
            "TYPE": type_,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            entity: Text,
            property_code: Text,
            *,
            property_new: Optional[Text] = None,
            name: Optional[Text] = None,
            type_: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "ENTITY": entity,
            "PROPERTY": property_code,
        }

        if property_new is not None:
            params["PROPERTY_NEW"] = property_new

        if name is not None:
            params["NAME"] = name

        if type_ is not None:
            params["TYPE"] = type_

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            entity: Text,
            property_code: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "ENTITY": entity,
            "PROPERTY": property_code,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

