from typing import Optional, Text, Union

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Sender",
]


class Sender(BaseEntity):
    """"""

    @type_checker
    def add(
            self,
            code: Text,
            type: Text,
            handler: Text,
            name: Union[Text, JSONDict],
            *,
            description: Optional[Union[Text, JSONDict]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "CODE": code,
            "TYPE": type,
            "HANDLER": handler,
            "NAME": name,
        }

        if description is not None:
            params["DESCRIPTION"] = description

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            code: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "CODE": code,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            code: Text,
            *,
            handler: Optional[Text] = None,
            name: Optional[Union[Text, JSONDict]] = None,
            description: Optional[Union[Text, JSONDict]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "CODE": code,
        }

        if handler is not None:
            params["HANDLER"] = handler

        if name is not None:
            params["NAME"] = name

        if description is not None:
            params["DESCRIPTION"] = description

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
