from typing import Iterable, Optional, Text

from ..._bitrix_api_request import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict

from ..base import Base


class BaseCRM(Base):
    """"""

    ENTITY_TYPE_ID: Optional[int] = None
    """Numeric Identifier of Type."""

    ENTITY_TYPE_NAME: Optional[Text] = None
    """Symbolic Code of Type."""

    ENTITY_TYPE_ABBR: Optional[Text] = None
    """Short Symbolic Code of Type."""

    USER_FIELD_ENTITY_ID: Optional[Text] = None
    """User Field Object Type."""

    @type_checker
    def _fields(
            self,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """"""
        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self._fields),
            timeout=timeout,
        )

    @type_checker
    def _add(
            self,
            fields: JSONDict,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "fields": fields,
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self._add),
            params=params,
            timeout=timeout,
        )

    @type_checker
    def _get(
            self,
            bitrix_id: int,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self._get),
            params=params,
            timeout=timeout,
        )

    @type_checker
    def _list(
            self,
            *,
            select: Optional[Iterable[Text]] = None,
            filter: Optional[JSONDict] = None,
            order: Optional[JSONDict] = None,
            start: Optional[int] = None,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "start": start,
        }

        if select is not None:
            params["select"] = list(select)

        if filter is not None:
            params["filter"] = filter

        if order is not None:
            params["order"] = order

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self._list),
            params=params,
            timeout=timeout,
        )

    @type_checker
    def _update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
            "fields": fields,
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self._update),
            params=params,
            timeout=timeout,
        )

    @type_checker
    def _delete(
            self,
            bitrix_id: int,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self._delete),
            params=params,
            timeout=timeout,
        )
