from typing import Optional

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Files",
]


class Files(BaseEntity):
    """"""

    @type_checker
    def attach(
            self,
            task_id: int,
            file_id: int,
            *,
            params: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        payload = {
            "taskId": task_id,
            "fileId": file_id,
        }

        if params is not None:
            payload["params"] = params

        return self._make_bitrix_api_request(
            api_wrapper=self.attach,
            params=payload,
            timeout=timeout,
        )
