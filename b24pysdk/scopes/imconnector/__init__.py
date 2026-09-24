from functools import cached_property
from typing import Optional, Text, Union

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.converters import bool_to_bitrix
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_scope import BaseScope
from .chat import Chat
from .connector import Connector
from .delete import Delete
from .send import Send
from .update import Update

__all__ = [
    "Imconnector",
]


class Imconnector(BaseScope):
    """"""

    @cached_property
    def chat(self) -> Chat:
        """"""
        return Chat(self)

    @cached_property
    def connector(self) -> Connector:
        """"""
        return Connector(self)

    @cached_property
    def delete(self) -> Delete:
        """"""
        return Delete(self)

    @cached_property
    def send(self) -> Send:
        """"""
        return Send(self)

    @cached_property
    def update(self) -> Update:
        """"""
        return Update(self)

    @type_checker
    def activate(
            self,
            connector: Text,
            line: Union[int, Text],
            active: Union[bool, int],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if isinstance(active, bool):
            active = int(active)

        params = dict(
            CONNECTOR=connector,
            LINE=line,
            ACTIVE=active,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.activate,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            timeout=timeout,
        )

    @type_checker
    def register(
            self,
            bitrix_id: Text,
            name: Text,
            icon: JSONDict,
            placement_handler: Text,
            *,
            icon_disabled: Optional[JSONDict] = MISSING,
            del_external_messages: Optional[bool] = MISSING,
            edit_internal_messages: Optional[bool] = MISSING,
            del_internal_messages: Optional[bool] = MISSING,
            newsletter: Optional[bool] = MISSING,
            need_system_messages: Optional[bool] = MISSING,
            need_signature: Optional[bool] = MISSING,
            chat_group: Optional[bool] = MISSING,
            comment: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            ID=bitrix_id,
            NAME=name,
            ICON=icon,
            PLACEMENT_HANDLER=placement_handler,
        )

        if icon_disabled is not MISSING:
            params["ICON_DISABLED"] = icon_disabled

        if del_external_messages is not MISSING:
            params["DEL_EXTERNAL_MESSAGES"] = bool_to_bitrix(del_external_messages, is_required=True)

        if edit_internal_messages is not MISSING:
            params["EDIT_INTERNAL_MESSAGES"] = bool_to_bitrix(edit_internal_messages, is_required=True)

        if del_internal_messages is not MISSING:
            params["DEL_INTERNAL_MESSAGES"] = bool_to_bitrix(del_internal_messages, is_required=True)

        if newsletter is not MISSING:
            params["NEWSLETTER"] = bool_to_bitrix(newsletter, is_required=True)

        if need_system_messages is not MISSING:
            params["NEED_SYSTEM_MESSAGES"] = bool_to_bitrix(need_system_messages, is_required=True)

        if need_signature is not MISSING:
            params["NEED_SIGNATURE"] = bool_to_bitrix(need_signature, is_required=True)

        if chat_group is not MISSING:
            params["CHAT_GROUP"] = bool_to_bitrix(chat_group, is_required=True)

        if comment is not MISSING:
            params["COMMENT"] = comment

        return self._make_bitrix_api_request(
            api_wrapper=self.register,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def status(
            self,
            connector: Text,
            *,
            line: Optional[Union[int, Text]] = MISSING,
            error: Optional[bool] = MISSING,
            configured: Optional[bool] = MISSING,
            status: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            CONNECTOR=connector,
        )

        if line is not MISSING:
            params["LINE"] = line

        if error is not MISSING:
            params["ERROR"] = bool_to_bitrix(error, is_required=True)

        if configured is not MISSING:
            params["CONFIGURED"] = bool_to_bitrix(configured, is_required=True)

        if status is not MISSING:
            params["STATUS"] = bool_to_bitrix(status, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self.status,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def unregister(
            self,
            *,
            bitrix_id: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {}

        if bitrix_id is not MISSING:
            params["ID"] = bitrix_id

        return self._make_bitrix_api_request(
            api_wrapper=self.unregister,
            params=params or None,
            timeout=timeout,
        )
