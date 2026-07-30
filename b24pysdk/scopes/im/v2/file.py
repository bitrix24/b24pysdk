from typing import Text

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
            dialog_id: Text,
            file_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "dialogId": dialog_id,
            "fileId": file_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.download,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def upload(
            self,
            dialog_id: Text,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "dialogId": dialog_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.upload,
            params=params,
            timeout=timeout,
        )
