from typing import Iterable, Optional, Text, Union

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import B24BoolStrict, JSONDict, JSONList, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Command",
]


class Command(BaseEntity):
    """"""

    @type_checker
    def answer(
            self,
            message_id: int,
            message: Text,
            *,
            command_id: Optional[int] = None,
            command: Optional[Text] = None,
            attach: Optional[JSONDict] = None,
            keyboard: Optional[JSONDict] = None,
            menu: Optional[JSONList] = None,
            system: Optional[Text] = None,
            url_preview: Optional[Text] = None,
            client_id: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "MESSAGE_ID": message_id,
            "MESSAGE": message,
        }

        if command_id is not None:
            params["COMMAND_ID"] = command_id

        if command is not None:
            params["COMMAND"] = command

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
            common: Optional[Union[bool, B24BoolStrict]] = None,
            hidden: Optional[Union[bool, B24BoolStrict]] = None,
            extranet_support: Optional[Union[bool, B24BoolStrict]] = None,
            client_id: Optional[Text] = None,
            event_command_add: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if lang.__class__ is not list:
            lang = list(lang)

        params = {
            "BOT_ID": bot_id,
            "COMMAND": command,
            "LANG": lang,
        }

        if common is not None:
            params["COMMON"] = B24BoolStrict(common).to_b24()

        if hidden is not None:
            params["HIDDEN"] = B24BoolStrict(hidden).to_b24()

        if extranet_support is not None:
            params["EXTRANET_SUPPORT"] = B24BoolStrict(extranet_support).to_b24()

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

        params = {
            "COMMAND_ID": command_id,
            "FIELDS": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unregister(
            self,
            command_id: int,
            *,
            client_id: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "COMMAND_ID": command_id,
        }

        if client_id is not None:
            params["CLIENT_ID"] = client_id

        return self._make_bitrix_api_request(
            api_wrapper=self.unregister,
            params=params,
            timeout=timeout,
        )
