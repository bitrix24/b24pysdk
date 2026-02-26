from functools import cached_property
from typing import Optional, Text, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity
from .another import Another

__all__ = [
    "Operator",
]


class Operator(BaseEntity):
    """"""

    @type_checker
    def answer(
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
            api_wrapper=self.answer,
            params=params or None,
            timeout=timeout,
        )

    @cached_property
    def another(self) -> Another:
        """"""
        return Another(self)

    @type_checker
    def finish(
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
            api_wrapper=self.finish,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def skip(
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
            api_wrapper=self.skip,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def spam(
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
            api_wrapper=self.spam,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def transfer(
            self,
            *,
            chat_id: Optional[Union[int, Text]] = None,
            transfer_id: Optional[Union[int, Text]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if chat_id is not None:
            params["CHAT_ID"] = chat_id

        if transfer_id is not None:
            params["TRANSFER_ID"] = transfer_id

        return self._make_bitrix_api_request(
            api_wrapper=self.transfer,
            params=params or None,
            timeout=timeout,
        )
