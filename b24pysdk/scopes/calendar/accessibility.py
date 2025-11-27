from typing import Iterable, Text

from ...bitrix_api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Accessibility",
]


class Accessibility(BaseEntity):
    """"""

    @type_checker
    def get(
            self,
            users: Iterable[int],
            from_date: Text,
            to: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if users.__class__ is not list:
            users = list(users)

        params = {
            "users": users,
            "from": from_date,
            "to": to,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

