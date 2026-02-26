from typing import Optional, Text, Union

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import B24BoolStrict, JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Message",
]


class Message(BaseEntity):
    """"""

    @type_checker
    def add(
            self,
            dialog_id: Text,
            message: Text,
            *,
            system: Optional[Union[bool, B24BoolStrict]] = None,
            attach: Optional[JSONDict] = None,
            url_preview: Optional[Union[bool, B24BoolStrict]] = None,
            keyboard: Optional[JSONDict] = None,
            menu: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            DIALOG_ID=dialog_id,
            MESSAGE=message,
        )

        if system is not None:
            params["SYSTEM"] = B24BoolStrict(system).to_b24()

        if attach is not None:
            params["ATTACH"] = attach

        if url_preview is not None:
            params["URL_PREVIEW"] = B24BoolStrict(url_preview).to_b24()

        if keyboard is not None:
            params["KEYBOARD"] = keyboard

        if menu is not None:
            params["MENU"] = menu

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def command(
            self,
            message_id: Union[int, Text],
            bot_id: Union[int, Text],
            command: Text,
            command_params: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            MESSAGE_ID=message_id,
            BOT_ID=bot_id,
            COMMAND=command,
            COMMAND_PARAMS=command_params,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.command,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            message_id: Union[int, Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            MESSAGE_ID=message_id,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def like(
            self,
            message_id: Union[int, Text],
            *,
            action: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            MESSAGE_ID=message_id,
        )

        if action is not None:
            params["ACTION"] = action

        return self._make_bitrix_api_request(
            api_wrapper=self.like,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def share(
            self,
            message_id: Union[int, Text],
            dialog_id: Text,
            type: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            MESSAGE_ID=message_id,
            DIALOG_ID=dialog_id,
            TYPE=type,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.share,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            message_id: Union[int, Text],
            *,
            message: Optional[Text] = None,
            attach: Optional[JSONDict] = None,
            url_preview: Optional[Union[bool, B24BoolStrict]] = None,
            keyboard: Optional[JSONDict] = None,
            menu: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            MESSAGE_ID=message_id,
        )

        if message is not None:
            params["MESSAGE"] = message

        if attach is not None:
            params["ATTACH"] = attach

        if url_preview is not None:
            params["URL_PREVIEW"] = B24BoolStrict(url_preview).to_b24()

        if keyboard is not None:
            params["KEYBOARD"] = keyboard

        if menu is not None:
            params["MENU"] = menu

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
