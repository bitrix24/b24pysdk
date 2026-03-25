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
    def add(  # noqa: C901
            self,
            message: Text,
            *,
            dialog_id: Optional[Text] = None,
            from_user_id: Optional[int] = None,
            to_user_id: Optional[int] = None,
            bot_id: Optional[int] = None,
            attach: Optional[Union[JSONDict, Text]] = None,
            keyboard: Optional[Union[JSONDict, Text]] = None,
            menu: Optional[Union[JSONDict, Text]] = None,
            system: Optional[Union[bool, B24BoolStrict]] = None,
            url_preview: Optional[Union[bool, B24BoolStrict]] = None,
            skip_connector: Optional[Union[bool, B24BoolStrict]] = None,
            client_id: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "MESSAGE": message,
        }

        if dialog_id is not None:
            params["DIALOG_ID"] = dialog_id

        if from_user_id is not None:
            params["FROM_USER_ID"] = from_user_id

        if to_user_id is not None:
            params["TO_USER_ID"] = to_user_id

        if bot_id is not None:
            params["BOT_ID"] = bot_id

        if attach is not None:
            params["ATTACH"] = attach

        if keyboard is not None:
            params["KEYBOARD"] = keyboard

        if menu is not None:
            params["MENU"] = menu

        if system is not None:
            params["SYSTEM"] = B24BoolStrict(system).to_b24()

        if url_preview is not None:
            params["URL_PREVIEW"] = B24BoolStrict(url_preview).to_b24()

        if skip_connector is not None:
            params["SKIP_CONNECTOR"] = B24BoolStrict(skip_connector).to_b24()

        if client_id is not None:
            params["CLIENT_ID"] = client_id

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
            client_id: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "MESSAGE_ID": message_id,
        }

        if bot_id is not None:
            params["BOT_ID"] = bot_id

        if complete is not None:
            params["COMPLETE"] = complete

        if client_id is not None:
            params["CLIENT_ID"] = client_id

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
            url_preview: Optional[Union[bool, B24BoolStrict]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "MESSAGE_ID": message_id,
        }

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
            params["URL_PREVIEW"] = B24BoolStrict(url_preview).to_b24()

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def like(
            self,
            message_id: int,
            *,
            bot_id: Optional[int] = None,
            action: Optional[Text] = None,
            client_id: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "MESSAGE_ID": message_id,
        }

        if bot_id is not None:
            params["BOT_ID"] = bot_id

        if action is not None:
            params["ACTION"] = action

        if client_id is not None:
            params["CLIENT_ID"] = client_id

        return self._make_bitrix_api_request(
            api_wrapper=self.like,
            params=params,
            timeout=timeout,
        )
