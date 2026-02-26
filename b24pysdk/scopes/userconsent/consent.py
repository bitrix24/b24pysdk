from typing import Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Consent",
]


class Consent(BaseEntity):
    """"""

    @type_checker
    def add(
            self,
            *,
            agreement_id: Optional[Text] = None,
            ip: Optional[Text] = None,
            url: Optional[Text] = None,
            origin_id: Optional[Text] = None,
            originator_id: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if agreement_id is not None:
            params["agreement_id"] = agreement_id

        if ip is not None:
            params["ip"] = ip

        if url is not None:
            params["url"] = url

        if origin_id is not None:
            params["origin_id"] = origin_id

        if originator_id is not None:
            params["originator_id"] = originator_id

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params or None,
            timeout=timeout,
        )
