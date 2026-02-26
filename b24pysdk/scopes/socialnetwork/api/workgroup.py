from typing import Iterable, Optional, Text, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import B24BoolStrict, JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Workgroup",
]


class Workgroup(BaseEntity):
    """"""

    @type_checker
    def get(
            self,
            params: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        _params = {
            "params": params,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=_params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            filter: Optional[JSONDict] = None,
            select: Optional[Iterable[Text]] = None,
            is_admin: Optional[Union[bool, B24BoolStrict]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if filter is not None:
            params["filter"] = filter

        if select is not None:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        if is_admin is not None:
            params["IS_ADMIN"] = B24BoolStrict(is_admin).to_b24()

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
