from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "File",
]


class File(BaseEntity):
    """"""

    @type_checker
    def attach(
            self,
            task_id: int,
            file_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "taskId": task_id,
            "fileIds": file_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.attach,
            params=params,
            timeout=timeout,
        )
