from typing import Iterable, Optional, Text

from ....api.requests import BitrixAPIRequest
from ....utils.functional import classproperty, type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Document",
]


class Document(BaseEntity):
    """"""

    @classproperty
    def _name(cls) -> Text:
        return "document"

    @type_checker
    def list(
            self,
            select: Iterable[Text],
            filter: JSONDict,
            *,
            order: Optional[JSONDict] = None,
            start: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if select.__class__ is not list:
            select = list(select)

        params: JSONDict = dict()
        params["select"] = select
        params["filter"] = filter

        if order is not None:
            params["order"] = order

        if start is not None:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            document_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = dict()
        params["documentId"] = document_id
        params["fields"] = fields

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
