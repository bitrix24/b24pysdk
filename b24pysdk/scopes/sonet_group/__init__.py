from functools import cached_property
from typing import Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import classproperty, type_checker
from ...utils.types import JSONDict, Timeout
from .._base_scope import BaseScope
from .feature import Feature
from .user import User

__all__ = [
    "SonetGroup",
]


class SonetGroup(BaseScope):
    """"""

    @classproperty
    def _name(cls) -> Text:
        return "sonet_group"

    @cached_property
    def feature(self) -> Feature:
        """"""
        return Feature(self)

    @cached_property
    def user(self) -> User:
        """"""
        return User(self)

    @type_checker
    def create(
            self,
            ar_fields: JSONDict,
            *,
            b_auto_subscribe: Optional[bool] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "arFields": ar_fields,
        }

        if b_auto_subscribe is not None:
            params["bAutoSubscribe"] = b_auto_subscribe

        return self._make_bitrix_api_request(
            api_wrapper=self.create,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            group_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "GROUP_ID": group_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            *,
            order: Optional[JSONDict] = None,
            filter: Optional[JSONDict] = None,
            is_admin: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if order is not None:
            params["ORDER"] = order

        if filter is not None:
            params["FILTER"] = filter

        if is_admin is not None:
            params["IS_ADMIN"] = is_admin

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def setowner(
            self,
            group_id: int,
            user_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "GROUP_ID": group_id,
            "USER_ID": user_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.setowner,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            group_id: int,
            *,
            name: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "GROUP_ID": group_id,
        }

        if name is not None:
            params["NAME"] = name

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
