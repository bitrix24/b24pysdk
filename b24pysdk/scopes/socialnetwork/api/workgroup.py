from typing import Iterable, Optional, Text

from ...._constants import MISSING
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
            filter: Optional[JSONDict] = MISSING,
            select: Optional[Iterable[Text]] = MISSING,
            order: Optional[JSONDict] = MISSING,
            params: Optional[JSONDict] = MISSING,
            start: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        _params: JSONDict = {}

        if filter is not MISSING:
            _params["filter"] = filter

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)

            _params["select"] = select

        if order is not MISSING:
            _params["order"] = order

        if params is not MISSING:
            _params["params"] = params

        if start is not MISSING:
            _params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=_params,
            timeout=timeout,
        )
