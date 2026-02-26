from functools import cached_property
from typing import Text, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity
from .messages import Messages
from .users import Users

__all__ = [
    "Dialog",
]


class Dialog(BaseEntity):
    """"""

    @type_checker
    def get(
            self,
            dialog_id: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            DIALOG_ID=dialog_id,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def read_all(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        return self._make_bitrix_api_request(
            api_wrapper=self.read_all,
            timeout=timeout,
        )

    @cached_property
    def messages(self) -> Messages:
        """"""
        return Messages(self)

    @type_checker
    def read(
            self,
            dialog_id: Text,
            message_id: Union[int, Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            DIALOG_ID=dialog_id,
            MESSAGE_ID=message_id,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.read,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unread(
            self,
            dialog_id: Text,
            message_id: Union[int, Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            DIALOG_ID=dialog_id,
            MESSAGE_ID=message_id,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.unread,
            params=params,
            timeout=timeout,
        )

    @cached_property
    def users(self) -> Users:
        """"""
        return Users(self)

    @type_checker
    def writing(
            self,
            dialog_id: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            DIALOG_ID=dialog_id,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.writing,
            params=params,
            timeout=timeout,
        )
