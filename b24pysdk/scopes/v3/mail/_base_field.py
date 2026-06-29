from typing import Iterable, Optional, Text

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity


class _BaseField(BaseEntity):
    """"""

    @type_checker
    def get(
            self,
            name: Text,
            *,
            select: Optional[Iterable[Text]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "name": name,
        }

        if select is not None:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            select: Iterable[Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if select.__class__ is not list:
            select = list(select)

        params = {
            "select": select,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
