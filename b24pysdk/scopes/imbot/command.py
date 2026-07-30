from typing import Iterable, Optional, Text, Union

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import B24BoolStrict, JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Command",
]


class Command(BaseEntity):
    """"""

    @type_checker
    def register(
            self,
            bot_id: int,
            command: Text,
            lang: Iterable[JSONDict],
            *,
            common: Optional[Union[bool, B24BoolStrict]] = MISSING,
            hidden: Optional[Union[bool, B24BoolStrict]] = MISSING,
            extranet_support: Optional[Union[bool, B24BoolStrict]] = MISSING,
            client_id: Optional[Text] = MISSING,
            event_command_add: Optional[Text] = MISSING,
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

        if common is not MISSING:
            params["COMMON"] = B24BoolStrict(common).to_b24()

        if hidden is not MISSING:
            params["HIDDEN"] = B24BoolStrict(hidden).to_b24()

        if extranet_support is not MISSING:
            params["EXTRANET_SUPPORT"] = B24BoolStrict(extranet_support).to_b24()

        if client_id is not MISSING:
            params["CLIENT_ID"] = client_id

        if event_command_add is not MISSING:
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
            client_id: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "COMMAND_ID": command_id,
        }

        if client_id is not MISSING:
            params["CLIENT_ID"] = client_id

        return self._make_bitrix_api_request(
            api_wrapper=self.unregister,
            params=params,
            timeout=timeout,
        )
