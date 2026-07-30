from typing import Optional, Text

from .._constants import MISSING
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
            active: Optional[bool] = MISSING,
            server: Optional[Text] = MISSING,
            port: Optional[int] = MISSING,
            link: Optional[Text] = MISSING,
            sort: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "NAME": name,
            "ENCRYPTION": B24Bool(encryption).to_b24(),
        }

        if active is not MISSING:
            params["ACTIVE"] = B24Bool(active).to_b24()

        if server is not MISSING:
            params["SERVER"] = server

        if port is not MISSING:
            params["PORT"] = port

        if link is not MISSING:
            params["LINK"] = link

        if sort is not MISSING:
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
            active: Optional[bool] = MISSING,
            name: Optional[Text] = MISSING,
            server: Optional[Text] = MISSING,
            port: Optional[int] = MISSING,
            encryption: Optional[bool] = MISSING,
            link: Optional[Text] = MISSING,
            sort: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "ID": bitrix_id,
        }

        if active is not MISSING:
            params["ACTIVE"] = B24Bool(active).to_b24()

        if name is not MISSING:
            params["NAME"] = name

        if server is not MISSING:
            params["SERVER"] = server

        if port is not MISSING:
            params["PORT"] = port

        if encryption is not MISSING:
            params["ENCRYPTION"] = B24Bool(encryption).to_b24()

        if link is not MISSING:
            params["LINK"] = link

        if sort is not MISSING:
            params["SORT"] = sort

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
