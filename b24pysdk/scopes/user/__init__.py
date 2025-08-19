from typing import TYPE_CHECKING

from ...bitrix_api.classes import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import Timeout
from ..scope import Scope

if TYPE_CHECKING:
    from ... import Client

__all__ = [
    "User",
]


class User(Scope):
    """"""

    def __init__(self, client: "Client"):
        super().__init__(client)

    @type_checker
    def fields(
            self,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._make_bitrix_api_request(
            api_method=self.fields,
            timeout=timeout,
        )
