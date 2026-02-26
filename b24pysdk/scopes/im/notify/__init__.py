from functools import cached_property
from typing import Optional, Text

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity
from .personal import Personal
from .read import Read
from .system import System

__all__ = [
    "Notify",
]


class Notify(BaseEntity):
    """"""

    @type_checker
    def answer(
            self,
            bitrix_id: int,
            answer_text: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "ID": bitrix_id,
            "ANSWER_TEXT": answer_text,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.answer,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def confirm(
            self,
            bitrix_id: int,
            notify_value: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "ID": bitrix_id,
            "NOTIFY_VALUE": notify_value,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.confirm,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            *,
            bitrix_id: Optional[int] = None,
            tag: Optional[Text] = None,
            sub_tag: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if bitrix_id is not None:
            params["ID"] = bitrix_id

        if tag is not None:
            params["TAG"] = tag

        if sub_tag is not None:
            params["SUB_TAG"] = sub_tag

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params or None,
            timeout=timeout,
        )

    @cached_property
    def personal(self) -> Personal:
        """"""
        return Personal(self)

    @cached_property
    def read(self) -> Read:
        """"""
        return Read(self)

    @cached_property
    def system(self) -> System:
        """"""
        return System(self)
