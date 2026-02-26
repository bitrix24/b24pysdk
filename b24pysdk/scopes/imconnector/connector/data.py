from typing import Text, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Data",
]


class Data(BaseEntity):
    """"""

    @type_checker
    def set(
            self,
            connector: Text,
            line: Union[int, Text],
            data: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            CONNECTOR=connector,
            LINE=line,
            DATA=data,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.set,
            params=params,
            timeout=timeout,
        )
