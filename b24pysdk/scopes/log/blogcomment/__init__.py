from functools import cached_property
from typing import Iterable, Optional, Sequence, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import classproperty, type_checker
from ....utils.types import B24File, JSONDict, Timeout
from ..._base_entity import BaseEntity
from .user import User

__all__ = [
    "Blogcomment",
]


class Blogcomment(BaseEntity):
    """"""

    @classproperty
    def _name(cls) -> Text:
        """"""
        return "blogcomment"

    @cached_property
    def user(self) -> User:
        """"""
        return User(self)

    @type_checker
    def add(
            self,
            post_id: int,
            text: Text,
            *,
            user_id: Optional[int] = MISSING,
            files: Iterable[Sequence[Text]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "POST_ID": post_id,
            "TEXT": text,
        }

        if user_id is not MISSING:
            params["USER_ID"] = user_id

        if files is not MISSING:
            params["FILES"] = [B24File(file).to_b24() for file in files]

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            comment_id: int,
            *,
            user_id: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "COMMENT_ID": comment_id,
        }

        if user_id is not MISSING:
            params["USER_ID"] = user_id

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )
