from typing import Iterable, Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.converters import bool_to_bitrix
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
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
            common: Optional[bool] = MISSING,
            hidden: Optional[bool] = MISSING,
            extranet_support: Optional[bool] = MISSING,
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
            params["COMMON"] = bool_to_bitrix(common, is_required=True)

        if hidden is not MISSING:
            params["HIDDEN"] = bool_to_bitrix(hidden, is_required=True)

        if extranet_support is not MISSING:
            params["EXTRANET_SUPPORT"] = bool_to_bitrix(extranet_support, is_required=True)

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
