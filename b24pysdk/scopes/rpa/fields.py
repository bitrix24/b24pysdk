from typing import Iterable, Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Fields",
]


class Fields(BaseEntity):
    """"""

    @type_checker
    def get_settings(
            self,
            type_id: int,
            *,
            stage_id: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "typeId": type_id,
        }

        if stage_id is not None:
            params["stageId"] = stage_id

        return self._make_bitrix_api_request(
            api_wrapper=self.get_settings,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set_settings(
            self,
            type_id: int,
            fields: JSONDict,
            *,
            stage_id: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "typeId": type_id,
            "fields": fields,
        }

        if stage_id is not None:
            params["stageId"] = stage_id

        return self._make_bitrix_api_request(
            api_wrapper=self.set_settings,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set_visibility_settings(
            self,
            type_id: int,
            visibility: Text,
            fields: Iterable[Text],
            *,
            stage_id: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if fields.__class__ is not list:
            fields = list(fields)

        params: JSONDict = {
            "typeId": type_id,
            "visibility": visibility,
            "fields": fields,
        }

        if stage_id is not None:
            params["stageId"] = stage_id

        return self._make_bitrix_api_request(
            api_wrapper=self.set_visibility_settings,
            params=params,
            timeout=timeout,
        )
