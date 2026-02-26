from typing import Optional, Text, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import B24BoolStrict, Timeout
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
            *,
            upload_id: Optional[Union[int, Text]] = None,
            disk_id: Optional[Union[int, Text]] = None,
            message: Optional[Text] = None,
            silent_mode: Optional[Union[bool, B24BoolStrict]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            CHAT_ID=chat_id,
        )

        if upload_id is not None:
            params["UPLOAD_ID"] = upload_id

        if disk_id is not None:
            params["DISK_ID"] = disk_id

        if message is not None:
            params["MESSAGE"] = message

        if silent_mode is not None:
            params["SILENT_MODE"] = B24BoolStrict(silent_mode).to_b24()

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
    ) -> BitrixAPIRequest:
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
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            DISK_ID=disk_id,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.save,
            params=params,
            timeout=timeout,
        )
