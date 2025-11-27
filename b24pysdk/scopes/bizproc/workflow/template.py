from typing import Iterable, Optional, Text

from ....bitrix_api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Template",
]


class Template(BaseEntity):
    """"""

    @type_checker
    def add(
            self,
            document_type: Iterable,
            name: Text,
            template_data: bytes,
            *,
            description: Optional[Text] = None,
            auto_execute: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "DOCUMENT_TYPE": document_type,
            "NAME": name,
            "TEMPLATE_DATA": template_data,
        }

        if description is not None:
            params["DESCRIPTION"] = description

        if description is not None:
            params["AUTO_EXECUTE"] = auto_execute

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            code: Text,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "CODE": code,
            "FIELDS": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            code: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "CODE": code,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            timeout=timeout,
        )
