from functools import cached_property
from typing import Optional, Text, Union

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
            icon_disabled: Optional[JSONDict] = None,
            del_external_messages: Optional[Union[bool, B24BoolStrict]] = None,
            edit_internal_messages: Optional[Union[bool, B24BoolStrict]] = None,
            del_internal_messages: Optional[Union[bool, B24BoolStrict]] = None,
            newsletter: Optional[Union[bool, B24BoolStrict]] = None,
            need_system_messages: Optional[Union[bool, B24BoolStrict]] = None,
            need_signature: Optional[Union[bool, B24BoolStrict]] = None,
            chat_group: Optional[Union[bool, B24BoolStrict]] = None,
            comment: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            ID=bitrix_id,
            NAME=name,
            ICON=icon,
            PLACEMENT_HANDLER=placement_handler,
        )

        if icon_disabled is not None:
            params["ICON_DISABLED"] = icon_disabled

        if del_external_messages is not None:
            params["DEL_EXTERNAL_MESSAGES"] = B24BoolStrict(del_external_messages).to_b24()

        if edit_internal_messages is not None:
            params["EDIT_INTERNAL_MESSAGES"] = B24BoolStrict(edit_internal_messages).to_b24()

        if del_internal_messages is not None:
            params["DEL_INTERNAL_MESSAGES"] = B24BoolStrict(del_internal_messages).to_b24()

        if newsletter is not None:
            params["NEWSLETTER"] = B24BoolStrict(newsletter).to_b24()

        if need_system_messages is not None:
            params["NEED_SYSTEM_MESSAGES"] = B24BoolStrict(need_system_messages).to_b24()

        if need_signature is not None:
            params["NEED_SIGNATURE"] = B24BoolStrict(need_signature).to_b24()

        if chat_group is not None:
            params["CHAT_GROUP"] = B24BoolStrict(chat_group).to_b24()

        if comment is not None:
            params["COMMENT"] = comment

        return self._make_bitrix_api_request(
            api_wrapper=self.register,
            params=params,
            timeout=timeout,
        )

    @cached_property
    def send(self) -> Send:
        """"""
        return Send(self)

    @type_checker
    def status(
            self,
            *,
            line: Optional[Union[int, Text]] = None,
            connector: Optional[Text] = None,
            error: Optional[Union[bool, B24BoolStrict]] = None,
            configured: Optional[Union[bool, B24BoolStrict]] = None,
            status: Optional[Union[bool, B24BoolStrict]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if line is not None:
            params["LINE"] = line

        if connector is not None:
            params["CONNECTOR"] = connector

        if error is not None:
            params["ERROR"] = B24BoolStrict(error).to_b24()

        if configured is not None:
            params["CONFIGURED"] = B24BoolStrict(configured).to_b24()

        if status is not None:
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
            bitrix_id: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if bitrix_id is not None:
            params["ID"] = bitrix_id

        return self._make_bitrix_api_request(
            api_wrapper=self.unregister,
            params=params or None,
            timeout=timeout,
        )

    @cached_property
    def update(self) -> Update:
        """"""
        return Update(self)
