from typing import TYPE_CHECKING, Iterable, Optional, Text

from ...bitrix_api.classes import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from ..base import Base

if TYPE_CHECKING:
    from .api import API


class Workgroup(Base):
    """"""

    def __init__(self, api: "API"):
        super().__init__(api._scope)
        self._path = self._get_path(api)

    @type_checker
    def get(
            self,
            params: JSONDict,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "params": params,
        }

        return self._make_bitrix_api_request(
            api_method=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            filter: Optional[JSONDict] = None,
            select: Optional[Iterable[Text]] = None,
            is_admin: Optional[bool] = None,
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
            params["IS_ADMIN"] = is_admin

        return self._make_bitrix_api_request(
            api_method=self.list,
            params=params,
            timeout=timeout,
        )
