from typing import Optional

from ...bitrix_api.classes import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from ..base import Base

__all__ = [
    "Userfield",
]


class Userfield(Base):
    """"""

    @type_checker
    def add(
            self,
            fields: JSONDict,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_method=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            order: Optional[JSONDict] = None,
            filter: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if order is not None:
            params["order"] = order

        if filter is not None:
            params["filter"] = filter

        return self._make_bitrix_api_request(
            api_method=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_method=self.update,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_method=self.delete,
            params=params,
            timeout=timeout,
        )
