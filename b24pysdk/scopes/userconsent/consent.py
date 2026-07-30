from typing import Optional, Text

from ..._constants import MISSING
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
            agreement_id: int,
            ip: Text,
            *,
            user_id: Optional[int] = MISSING,
            url: Optional[Text] = MISSING,
            origin_id: Optional[Text] = MISSING,
            originator_id: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "AGREEMENT_ID": agreement_id,
            "IP": ip,
        }

        if user_id is not MISSING:
            params["USER_ID"] = user_id

        if url is not MISSING:
            params["url"] = url

        if origin_id is not MISSING:
            params["origin_id"] = origin_id

        if originator_id is not MISSING:
            params["originator_id"] = originator_id

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params or None,
            timeout=timeout,
        )
