from typing import Iterable

from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "Slots",
]


class Slots(BaseEntity):
    """"""

    @type_checker
    def list(
            self,
            resource_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "resourceId": resource_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set(
            self,
            resource_id: int,
            slots: Iterable[JSONDict],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if slots.__class__ is not list:
            slots = list(slots)

        params = {
            "resourceId": resource_id,
            "slots": slots,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.set,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unset(
            self,
            resource_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "resourceID": resource_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.unset,
            params=params,
            timeout=timeout,
        )
