from typing import Optional, Text, Union

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.converters import bool_to_bitrix
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "File",
]


class File(BaseEntity):
    """"""

    @type_checker
    def commit(
            self,
            chat_id: Union[int, Text],
            upload_id: Union[int, Text],
            disk_id: Union[int, Text],
            *,
            message: Optional[Text] = MISSING,
            silent_mode: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """"""

        params = dict(
            CHAT_ID=chat_id,
            UPLOAD_ID=upload_id,
            DISK_ID=disk_id,
        )

        if message is not MISSING:
            params["MESSAGE"] = message

        if silent_mode is not MISSING:
            params["SILENT_MODE"] = bool_to_bitrix(silent_mode, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self.commit,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            chat_id: Union[int, Text],
            disk_id: Union[int, Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """"""

        params = dict(
            CHAT_ID=chat_id,
            DISK_ID=disk_id,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def save(
            self,
            disk_id: Union[int, Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """"""

        params = dict(
            DISK_ID=disk_id,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.save,
            params=params,
            timeout=timeout,
        )
