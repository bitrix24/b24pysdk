from typing import Optional, Text

from ...bitrix_api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Rights",
]


class Rights(BaseEntity):
    """"""

    @type_checker
    def get_tasks(
            self,
            bitrix_id: int,
            *,
            name: Optional[Text] = None,
            start: Optional[Text] = None,
            title: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "ID": bitrix_id,
        }

        if name is not None:
            params["NAME"] = name

        if start is not None:
            params["START"] = start

        if title is not None:
            params["TITLE"] = title

        return self._make_bitrix_api_request(
            api_wrapper=self.get_tasks,
            params=params,
            timeout=timeout,
        )

