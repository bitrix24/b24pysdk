from typing import Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import classproperty, type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Getusers",
]


class Getusers(BaseEntity):
    """"""

    @classproperty
    def _name(cls) -> Text:
        """"""
        return "getusers"

    @type_checker
    def important(
            self,
            post_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "POST_ID": post_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.important,
            params=params,
            timeout=timeout,
        )
