from typing import Iterable, Text

from .....api.requests import BitrixAPIRequest
from .....utils.functional import classproperty, type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "ExternalData",
]


class ExternalData(BaseEntity):
    """"""

    @classproperty
    def _name(cls) -> Text:
        return "externalData"

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
            external_data: Iterable[JSONDict],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if external_data.__class__ is not list:
            external_data = list(external_data)

        params = {
            "bookingId": booking_id,
            "externalData": external_data,
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
