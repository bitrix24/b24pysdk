from typing import Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
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
            bot_id: Optional[int] = None,
            attach: Optional[JSONDict] = None,
            keyboard: Optional[JSONDict] = None,
            menu: Optional[JSONDict] = None,
            system: Optional[Text] = None,
            url_preview: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()
        params["DIALOG_ID"] = dialog_id
        params["MESSAGE"] = message

        if bot_id is not None:
            params["BOT_ID"] = bot_id

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

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            message_id: int,
            *,
            bot_id: Optional[int] = None,
            complete: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()
        params["MESSAGE_ID"] = message_id

        if bot_id is not None:
            params["BOT_ID"] = bot_id

        if complete is not None:
            params["COMPLETE"] = complete

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            message_id: int,
            *,
            bot_id: Optional[int] = None,
            message: Optional[Text] = None,
            attach: Optional[JSONDict] = None,
            keyboard: Optional[JSONDict] = None,
            menu: Optional[JSONDict] = None,
            url_preview: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()
        params["MESSAGE_ID"] = message_id

        if bot_id is not None:
            params["BOT_ID"] = bot_id

        if message is not None:
            params["MESSAGE"] = message

        if attach is not None:
            params["ATTACH"] = attach

        if keyboard is not None:
            params["KEYBOARD"] = keyboard

        if menu is not None:
            params["MENU"] = menu

        if url_preview is not None:
            params["URL_PREVIEW"] = url_preview

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
