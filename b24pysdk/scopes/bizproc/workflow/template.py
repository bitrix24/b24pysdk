from typing import Iterable, Optional, Sequence, Text

from ....bitrix_api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import B24File, DocumentType, JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Template",
]


class Template(BaseEntity):
    """"""

    @type_checker
    def add(
            self,
            document_type: Sequence[Text],
            name: Text,
            template_data: Sequence[Text],
            *,
            description: Optional[Text] = None,
            auto_execute: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "DOCUMENT_TYPE": DocumentType(document_type).to_b24(),
            "NAME": name,
            "TEMPLATE_DATA": B24File(template_data).to_b24(),
        }

        if description is not None:
            params["DESCRIPTION"] = description

        if auto_execute is not None:
            params["AUTO_EXECUTE"] = auto_execute

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "ID": bitrix_id,
            "FIELDS": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            select: Optional[Iterable[Text]] = None,
            filter: Optional[JSONDict] = None,
            order: Optional[JSONDict] = None,
            start: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if select is not None:
            if select.__class__ is not list:
                select = list(select)

            params["SELECT"] = select

        if filter is not None:
            params["FILTER"] = filter

        if order is not None:
            params["ORDER"] = order

        if start is not None:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "ID": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )
