from typing import Optional, TYPE_CHECKING

from ....._bitrix_api_request import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict

from ...base_crm import BaseCRM

if TYPE_CHECKING:
    from .details import Details


class Configuration(BaseCRM):
    """"""

    def __init__(self, details: "Details"):
        super().__init__(details._scope)
        self._path = self._get_path(details)

    @type_checker
    def get(
            self,
            *,
            entity_type_id: int,
            user_id: Optional[int] = None,
            scope: Optional[str] = None,
            extras: Optional[JSONDict] = None,
            timeout: Optional[int] = None
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "entityTypeId": entity_type_id,
        }

        if user_id is not None:
            params["userId"] = user_id

        if scope is not None:
            params["scope"] = scope

        if extras is not None:
            params["extras"] = extras

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.get),
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set(
            self,
            *,
            entity_type_id: int,
            data: list[JSONDict],
            user_id: Optional[int],
            scope: Optional[str] = None,
            extras: Optional[JSONDict] = None,
            timeout: Optional[int] = None
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "entityTypeId": entity_type_id,
            "data": data,
        }

        if user_id is not None:
            params["userId"] = user_id

        if scope is not None:
            params["scope"] = scope

        if extras is not None:
            params["extras"] = extras

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.set),
            params=params,
            timeout=timeout,
        )

    @type_checker
    def reset(
            self,
            *,
            entity_type_id: int,
            user_id: Optional[int],
            scope: Optional[str] = None,
            extras: Optional[JSONDict] = None,
            timeout: Optional[int] = None
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "entityTypeId": entity_type_id,
        }

        if user_id is not None:
            params["userId"] = user_id

        if scope is not None:
            params["scope"] = scope

        if extras is not None:
            params["extras"] = extras

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.reset),
            params=params,
            timeout=timeout,
        )

    @type_checker
    def force_common_scope_for_all(
            self,
            *,
            entity_type_id: int,
            extras: Optional[JSONDict] = None,
            timeout: Optional[int] = None
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "entityTypeId": entity_type_id,
        }

        if extras is not None:
            params["extras"] = extras

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.force_common_scope_for_all),
            params=params,
            timeout=timeout,
        )
