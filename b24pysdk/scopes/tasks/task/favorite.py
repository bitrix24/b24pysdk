from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Favorite",
]


class Favorite(BaseEntity):
    """"""

    @type_checker
    def add(
            self,
            task_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "taskId": task_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def remove(
            self,
            task_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "taskId": task_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.remove,
            params=params,
            timeout=timeout,
        )
