from functools import cached_property
from typing import Optional, Text, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity
from .head import Head
from .history import History
from .mode import Mode

__all__ = [
    "Session",
]


class Session(BaseEntity):
    """"""

    @type_checker
    def intercept(
            self,
            *,
            chat_id: Optional[Union[int, Text]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if chat_id is not None:
            params["CHAT_ID"] = chat_id

        return self._make_bitrix_api_request(
            api_wrapper=self.intercept,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def join(
            self,
            chat_id: Union[int, Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            CHAT_ID=chat_id,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.join,
            params=params,
            timeout=timeout,
        )

    @cached_property
    def head(self) -> Head:
        """"""
        return Head(self)

    @cached_property
    def history(self) -> History:
        """"""
        return History(self)

    @cached_property
    def mode(self) -> Mode:
        """"""
        return Mode(self)

    @type_checker
    def open(
            self,
            user_code: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            USER_CODE=user_code,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.open,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def start(
            self,
            chat_id: Union[int, Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            CHAT_ID=chat_id,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.start,
            params=params,
            timeout=timeout,
        )
