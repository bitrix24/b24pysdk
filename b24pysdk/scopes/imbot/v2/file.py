from typing import Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import classproperty, type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "File",
]


class File(BaseEntity):
    """"""

    @classproperty
    def _name(cls) -> Text:
        """"""
        return "File"

    @type_checker
    def download(
            self,
            bot_id: int,
            file_id: int,
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "botId": bot_id,
            "fileId": file_id,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        return self._make_bitrix_api_request(
            api_wrapper=self.download,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def upload(
            self,
            bot_id: int,
            dialog_id: Text,
            fields: JSONDict,
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "botId": bot_id,
            "dialogId": dialog_id,
            "fields": fields,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        return self._make_bitrix_api_request(
            api_wrapper=self.upload,
            params=params,
            timeout=timeout,
        )
