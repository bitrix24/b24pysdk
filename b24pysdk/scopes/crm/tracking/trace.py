from typing import Iterable, Optional, Text

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from .._base_crm import BaseCRM

__all__ = [
    "Trace",
]


class Trace(BaseCRM):
    """"""

    @type_checker
    def add(
            self,
            trace: Text,
            *,
            entities: Optional[Iterable[JSONDict]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "TRACE": trace,
        }

        if entities is not None:
            if entities.__class__ is not list:
                entities = list(entities)

            params["ENTITIES"] = entities

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
        return self._delete(bitrix_id, timeout=timeout)
