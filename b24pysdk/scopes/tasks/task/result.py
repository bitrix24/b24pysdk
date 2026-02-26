from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Result",
]


class Result(BaseEntity):
    """"""

    @type_checker
    def add_from_comment(
            self,
            comment_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "commentId": comment_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add_from_comment,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete_from_comment(
            self,
            comment_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "commentId": comment_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete_from_comment,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            task_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "task_id": task_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
