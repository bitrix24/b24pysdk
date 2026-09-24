from typing import Iterable, Text

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "Value",
]


class Value(BaseEntity):
    """"""

    @type_checker
    def set(
            self,
            company: Text,
            data: Iterable[JSONDict],
            *,
            job: JSONDict = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """"""

        if data.__class__ is not list:
            data = list(data)

        params: JSONDict = {
            "company": company,
            "data": data,
        }

        if job is not MISSING:
            params["job"] = job

        return self._make_bitrix_api_request(
            api_wrapper=self.set,
            params=params,
            timeout=timeout,
        )
