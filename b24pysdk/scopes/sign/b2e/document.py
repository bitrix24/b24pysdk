from typing import Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Document",
]


class Document(BaseEntity):
    """"""

    @type_checker
    def get(
            self,
            uid: Text,
            *,
            language: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "uid": uid,
        }

        if language is not MISSING:
            params["language"] = language

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def send(
            self,
            fields: JSONDict,
            *,
            language: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "fields": fields,
        }

        if language is not MISSING:
            params["language"] = language

        return self._make_bitrix_api_request(
            api_wrapper=self.send,
            params=params,
            timeout=timeout,
        )
