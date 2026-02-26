from functools import cached_property
from typing import Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_scope import BaseScope
from .app import App
from .bot import Bot
from .chat import Chat
from .command import Command
from .dialog import Dialog
from .message import Message

__all__ = [
    "Imbot",
]


class Imbot(BaseScope):
    """"""

    @cached_property
    def app(self) -> App:
        """"""
        return App(self)

    @cached_property
    def bot(self) -> Bot:
        """"""
        return Bot(self)

    @cached_property
    def chat(self) -> Chat:
        """"""
        return Chat(self)

    @cached_property
    def command(self) -> Command:
        """"""
        return Command(self)

    @cached_property
    def dialog(self) -> Dialog:
        """"""
        return Dialog(self)

    @cached_property
    def message(self) -> Message:
        """"""
        return Message(self)

    @type_checker
    def register(
            self,
            code: Text,
            properties: JSONDict,
            *,
            event_handler: Optional[Text] = None,
            event_message_add: Optional[Text] = None,
            event_welcome_message: Optional[Text] = None,
            event_bot_delete: Optional[Text] = None,
            type: Optional[Text] = None,
            openline: Optional[Text] = None,
            client_id: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()
        params["CODE"] = code
        params["PROPERTIES"] = properties

        if event_handler is not None:
            params["EVENT_HANDLER"] = event_handler

        if event_message_add is not None:
            params["EVENT_MESSAGE_ADD"] = event_message_add

        if event_welcome_message is not None:
            params["EVENT_WELCOME_MESSAGE"] = event_welcome_message

        if event_bot_delete is not None:
            params["EVENT_BOT_DELETE"] = event_bot_delete

        if type is not None:
            params["TYPE"] = type

        if openline is not None:
            params["OPENLINE"] = openline

        if client_id is not None:
            params["CLIENT_ID"] = client_id

        return self._make_bitrix_api_request(
            api_wrapper=self.register,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unregister(
            self,
            *,
            bot_id: Optional[int] = None,
            client_id: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if bot_id is not None:
            params["BOT_ID"] = bot_id

        if client_id is not None:
            params["CLIENT_ID"] = client_id

        return self._make_bitrix_api_request(
            api_wrapper=self.unregister,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            bot_id: int,
            fields: JSONDict,
            *,
            client_id: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()
        params["BOT_ID"] = bot_id
        params["FIELDS"] = fields

        if client_id is not None:
            params["CLIENT_ID"] = client_id

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
