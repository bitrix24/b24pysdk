from typing import Optional, Text

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "Provider",
]


class Provider(BaseEntity):
    """"""

    @type_checker
    def list(
            self,
            *,
            company_uuid: Optional[Text] = MISSING,
            company_crm_id: Optional[int] = MISSING,
            language: Optional[Text] = MISSING,
            limit: Optional[int] = MISSING,
            offset: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {}

        if company_uuid is not MISSING:
            params["companyUuid"] = company_uuid

        if company_crm_id is not MISSING:
            params["companyCrmId"] = company_crm_id

        if language is not MISSING:
            params["language"] = language

        if limit is not MISSING:
            params["limit"] = limit

        if offset is not MISSING:
            params["offset"] = offset

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
