from typing import Iterable

from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "Client",
]


class Client(BaseEntity):
    """"""

    @type_checker
    def list(
            self,
            booking_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "bookingId": booking_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set(
            self,
            booking_id: int,
            clients: Iterable[JSONDict],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if clients.__class__ is not list:
            clients = list(clients)

        params = {
            "bookingId": booking_id,
            "clients": clients,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.set,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unset(
            self,
            booking_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "bookingId": booking_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.unset,
            params=params,
            timeout=timeout,
        )
