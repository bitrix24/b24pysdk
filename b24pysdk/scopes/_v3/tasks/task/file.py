from typing import Iterable

from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "File",
]


class File(BaseEntity):
    """"""

    @type_checker
    def attach(
            self,
            task_id: int,
            file_ids: Iterable[int],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if file_ids.__class__ is not list:
            file_ids = list(file_ids)

        params = {
            "taskId": task_id,
            "fileIds": file_ids,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.attach,
            params=params,
            timeout=timeout,
        )
