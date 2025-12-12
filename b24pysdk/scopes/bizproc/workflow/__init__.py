from functools import cached_property
from typing import Dict, Iterable, Optional, Sequence, Text

from ....bitrix_api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import DocumentType, JSONDict, Timeout
from ..._base_entity import BaseEntity
from .template import Template

__all__ = [
    "Workflow",
]


class Workflow(BaseEntity):
    """"""

    @cached_property
    def template(self) -> Template:
        """"""
        return Template(self)

    @type_checker
    def start(
            self,
            template_id: int,
            document_id: Sequence[Text],
            *,
            parameters: Optional[Dict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "TEMPLATE_ID": template_id,
            "DOCUMENT_ID": DocumentType(document_id).to_b24(),
        }

        if parameters is not None:
            params["PARAMETERS"] = parameters

        return self._make_bitrix_api_request(
            api_wrapper=self.start,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def instances(
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
            api_wrapper=self.instances,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def kill(
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
            api_wrapper=self.kill,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def terminate(
            self,
            bitrix_id: int,
            *,
            status: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "ID": bitrix_id,
        }

        if status is not None:
            params["STATUS"] = status

        return self._make_bitrix_api_request(
            api_wrapper=self.terminate,
            params=params,
            timeout=timeout,
        )
