from typing import Iterable, Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Command",
]


class Command(BaseEntity):
    """"""

    @type_checker
    def answer(  # noqa: C901
            self,
            *,
            command_id: Optional[int] = None,
            command: Optional[Text] = None,
            message_id: Optional[int] = None,
            message: Optional[Text] = None,
            attach: Optional[JSONDict] = None,
            keyboard: Optional[JSONDict] = None,
            menu: Optional[JSONDict] = None,
            system: Optional[Text] = None,
            url_preview: Optional[Text] = None,
            client_id: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if command_id is not None:
            params["COMMAND_ID"] = command_id

        if command is not None:
            params["COMMAND"] = command

        if message_id is not None:
            params["MESSAGE_ID"] = message_id

        if message is not None:
            params["MESSAGE"] = message

        if attach is not None:
            params["ATTACH"] = attach

        if keyboard is not None:
            params["KEYBOARD"] = keyboard

        if menu is not None:
            params["MENU"] = menu

        if system is not None:
            params["SYSTEM"] = system

        if url_preview is not None:
            params["URL_PREVIEW"] = url_preview

        if client_id is not None:
            params["CLIENT_ID"] = client_id

        return self._make_bitrix_api_request(
            api_wrapper=self.answer,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def register(
            self,
            bot_id: int,
            command: Text,
            lang: Iterable[JSONDict],
            *,
            common: Optional[Text] = None,
            hidden: Optional[Text] = None,
            extranet_support: Optional[Text] = None,
            client_id: Optional[Text] = None,
            event_command_add: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if lang.__class__ is not list:
            lang = list(lang)

        params = dict()
        params["BOT_ID"] = bot_id
        params["COMMAND"] = command
        params["LANG"] = lang

        if common is not None:
            params["COMMON"] = common

        if hidden is not None:
            params["HIDDEN"] = hidden

        if extranet_support is not None:
            params["EXTRANET_SUPPORT"] = extranet_support

        if client_id is not None:
            params["CLIENT_ID"] = client_id

        if event_command_add is not None:
            params["EVENT_COMMAND_ADD"] = event_command_add

        return self._make_bitrix_api_request(
            api_wrapper=self.register,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            command_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()
        params["COMMAND_ID"] = command_id
        params["FIELDS"] = fields

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
