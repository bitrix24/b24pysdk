from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Enum",
]


class Enum(BaseEntity):
    """"""

    @type_checker
    def get_round_types(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._make_bitrix_api_request(
            api_wrapper=self.get_round_types,
            timeout=timeout,
        )

    @type_checker
    def get_store_document_types(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._make_bitrix_api_request(
            api_wrapper=self.get_store_document_types,
            timeout=timeout,
        )
