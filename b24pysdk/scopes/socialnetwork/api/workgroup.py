from typing import Iterable, Optional, Text

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Workgroup",
]


class Workgroup(BaseEntity):
    """"""

    @type_checker
    def get(
            self,
            params: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        _params = {
            "params": params,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=_params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            filter: Optional[JSONDict] = None,
            select: Optional[Iterable[Text]] = None,
            order: Optional[JSONDict] = None,
            params: Optional[JSONDict] = None,
            start: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        _params: JSONDict = {}

        if filter is not None:
            _params["filter"] = filter

        if select is not None:
            if select.__class__ is not list:
                select = list(select)

            _params["select"] = select

        if order is not None:
            _params["order"] = order

        if params is not None:
            _params["params"] = params

        if start is not None:
            _params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=_params,
            timeout=timeout,
        )
