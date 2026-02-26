from typing import Iterable, Text, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Status",
]


class Status(BaseEntity):
    """"""

    @type_checker
    def delivery(
            self,
            connector: Text,
            line: Union[int, Text],
            messages: Iterable[JSONDict],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if messages.__class__ is not list:
            messages = list(messages)

        params = dict(
            CONNECTOR=connector,
            LINE=line,
            MESSAGES=messages,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.delivery,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def reading(
            self,
            connector: Text,
            line: Union[int, Text],
            messages: Iterable[JSONDict],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if messages.__class__ is not list:
            messages = list(messages)

        params = dict(
            CONNECTOR=connector,
            LINE=line,
            MESSAGES=messages,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.reading,
            params=params,
            timeout=timeout,
        )
