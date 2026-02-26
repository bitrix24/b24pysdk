from typing import Optional, Text

from ..api.requests import BitrixAPIRequest
from ..utils.functional import type_checker
from ..utils.types import B24Bool, Timeout
from ._base_scope import BaseScope

__all__ = [
    "Mailservice",
]


class Mailservice(BaseScope):
    """"""

    @type_checker
    def add(
            self,
            name: Text,
            encryption: bool,
            *,
            active: Optional[bool] = None,
            server: Optional[Text] = None,
            port: Optional[int] = None,
            link: Optional[Text] = None,
            sort: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            NAME=name,
            ENCRYPTION=B24Bool(encryption).to_b24(),
        )

        if active is not None:
            params["ACTIVE"] = B24Bool(active).to_b24()

        if server is not None:
            params["SERVER"] = server

        if port is not None:
            params["PORT"] = port

        if link is not None:
            params["LINK"] = link

        if sort is not None:
            params["SORT"] = sort

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

        params = {
            "ID": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._make_bitrix_api_request(
            api_wrapper=self.fields,
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

        params = {
            "ID": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
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
            bitrix_id: int,
            *,
            active: Optional[bool] = None,
            name: Optional[Text] = None,
            server: Optional[Text] = None,
            port: Optional[int] = None,
            encryption: Optional[bool] = None,
            link: Optional[Text] = None,
            sort: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "ID": bitrix_id,
        }

        if active is not None:
            params["ACTIVE"] = B24Bool(active).to_b24()

        if name is not None:
            params["NAME"] = name

        if server is not None:
            params["SERVER"] = server

        if port is not None:
            params["PORT"] = port

        if encryption is not None:
            params["ENCRYPTION"] = B24Bool(encryption).to_b24()

        if link is not None:
            params["LINK"] = link

        if sort is not None:
            params["SORT"] = sort

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
