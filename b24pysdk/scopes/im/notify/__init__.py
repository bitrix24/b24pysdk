from functools import cached_property
from typing import Annotated, Literal, Optional, Text, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import B24BoolStrict, JSONDict, Timeout
from ..._base_entity import BaseEntity
from .history import History
from .personal import Personal
from .read import Read
from .schema import Schema
from .system import System

__all__ = [
    "Notify",
]


class Notify(BaseEntity):
    """"""

    @cached_property
    def personal(self) -> Personal:
        """"""
        return Personal(self)

    @cached_property
    def history(self) -> History:
        """"""
        return History(self)

    @cached_property
    def read(self) -> Read:
        """"""
        return Read(self)

    @cached_property
    def schema(self) -> Schema:
        """"""
        return Schema(self)

    @cached_property
    def system(self) -> System:
        """"""
        return System(self)

    @type_checker
    def __call__(
            self,
            user_id: int,
            message: Text,
            *,
            type: Optional[Annotated[Text, Literal["USER", "SYSTEM"]]] = None,
            message_out: Optional[Text] = None,
            tag: Optional[Text] = None,
            sub_tag: Optional[Text] = None,
            attach: Optional[Union[JSONDict, Text]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "USER_ID": user_id,
            "MESSAGE": message,
        }

        if type is not None:
            params["TYPE"] = type

        if message_out is not None:
            params["MESSAGE_OUT"] = message_out

        if tag is not None:
            params["TAG"] = tag

        if sub_tag is not None:
            params["SUB_TAG"] = sub_tag

        if attach is not None:
            params["ATTACH"] = attach

        return self._make_bitrix_api_request(
            api_wrapper=self,
            params=params,
            timeout=timeout,
        )

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
            notify_value: Union[bool, B24BoolStrict],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "ID": bitrix_id,
            "NOTIFY_VALUE": B24BoolStrict(notify_value).to_b24(),
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
            client_id: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = dict()

        if bitrix_id is not None:
            params["ID"] = bitrix_id

        if tag is not None:
            params["TAG"] = tag

        if sub_tag is not None:
            params["SUB_TAG"] = sub_tag

        if client_id is not None:
            params["CLIENT_ID"] = client_id

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            *,
            last_id: Optional[int] = None,
            last_type: Optional[Literal[1, 3]] = None,
            limit: Optional[int] = None,
            convert_text: Optional[Union[bool, B24BoolStrict]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = dict()

        if last_id is not None:
            params["LAST_ID"] = last_id

        if last_type is not None:
            params["LAST_TYPE"] = last_type

        if limit is not None:
            params["LIMIT"] = limit

        if convert_text is not None:
            params["CONVERT_TEXT"] = B24BoolStrict(convert_text).to_b24()

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params or None,
            timeout=timeout,
        )
