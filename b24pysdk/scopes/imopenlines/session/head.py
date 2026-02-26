from typing import Optional, Text, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Head",
]


class Head(BaseEntity):
    """"""

    @type_checker
    def vote(
            self,
            session_id: Union[int, Text],
            *,
            rating: Optional[Union[int, Text]] = None,
            comment: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if rating is None and comment is None:
            raise ValueError("Either rating or comment must be provided.")

        params = dict(
            SESSION_ID=session_id,
        )

        if rating is not None:
            params["RATING"] = rating

        if comment is not None:
            params["COMMENT"] = comment

        return self._make_bitrix_api_request(
            api_wrapper=self.vote,
            params=params,
            timeout=timeout,
        )
