from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Dependence",
]


class Dependence(BaseEntity):
    """"""

    @type_checker
    def add(
            self,
            task_id_from: int,
            task_id_to: int,
            link_type: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "taskIdFrom": task_id_from,
            "taskIdTo": task_id_to,
            "linkType": link_type,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            task_id_from: int,
            task_id_to: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "taskIdFrom": task_id_from,
            "taskIdTo": task_id_to,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )
