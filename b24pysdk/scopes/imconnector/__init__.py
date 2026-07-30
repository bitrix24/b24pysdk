from functools import cached_property
from typing import Optional, Text, Union

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import B24BoolStrict, JSONDict, Timeout
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
            del_external_messages: Optional[Union[bool, B24BoolStrict]] = MISSING,
            edit_internal_messages: Optional[Union[bool, B24BoolStrict]] = MISSING,
            del_internal_messages: Optional[Union[bool, B24BoolStrict]] = MISSING,
            newsletter: Optional[Union[bool, B24BoolStrict]] = MISSING,
            need_system_messages: Optional[Union[bool, B24BoolStrict]] = MISSING,
            need_signature: Optional[Union[bool, B24BoolStrict]] = MISSING,
            chat_group: Optional[Union[bool, B24BoolStrict]] = MISSING,
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
            params["DEL_EXTERNAL_MESSAGES"] = B24BoolStrict(del_external_messages).to_b24()

        if edit_internal_messages is not MISSING:
            params["EDIT_INTERNAL_MESSAGES"] = B24BoolStrict(edit_internal_messages).to_b24()

        if del_internal_messages is not MISSING:
            params["DEL_INTERNAL_MESSAGES"] = B24BoolStrict(del_internal_messages).to_b24()

        if newsletter is not MISSING:
            params["NEWSLETTER"] = B24BoolStrict(newsletter).to_b24()

        if need_system_messages is not MISSING:
            params["NEED_SYSTEM_MESSAGES"] = B24BoolStrict(need_system_messages).to_b24()

        if need_signature is not MISSING:
            params["NEED_SIGNATURE"] = B24BoolStrict(need_signature).to_b24()

        if chat_group is not MISSING:
            params["CHAT_GROUP"] = B24BoolStrict(chat_group).to_b24()

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
            error: Optional[Union[bool, B24BoolStrict]] = MISSING,
            configured: Optional[Union[bool, B24BoolStrict]] = MISSING,
            status: Optional[Union[bool, B24BoolStrict]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            CONNECTOR=connector,
        )

        if line is not MISSING:
            params["LINE"] = line

        if error is not MISSING:
            params["ERROR"] = B24BoolStrict(error).to_b24()

        if configured is not MISSING:
            params["CONFIGURED"] = B24BoolStrict(configured).to_b24()

        if status is not MISSING:
            params["STATUS"] = B24BoolStrict(status).to_b24()

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
