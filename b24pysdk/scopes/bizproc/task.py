from typing import Iterable, Optional, Text

from ...bitrix_api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Task",
]


class Task(BaseEntity):
    """"""

    @type_checker
    def complete(
            self,
            task_id: Text,
            status: Text,
            *,
            comment: Optional[Text] = None,
            fields: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "TASK_ID": task_id,
            "STATUS": status,
        }

        if comment is not None:
            params["COMMENT"] = comment

        if fields is not None:
            params["FIELDS"] = fields

        return self._make_bitrix_api_request(
            api_wrapper=self.complete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delegate(
            self,
            task_ids: Iterable,
            from_user_id: int,
            to_user_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "TASK_IDS": task_ids,
            "FROM_USER_ID": from_user_id,
            "TO_USER_ID": to_user_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delegate,
            params=params,
            timeout=timeout,
        )
