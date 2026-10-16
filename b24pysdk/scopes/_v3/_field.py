from typing import Iterable, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIValueRequest, BitrixAPIValuesRequest
from ...schemas.v3.field import V3Field, V3FieldGetData, V3FieldListData
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._adapters import BitrixSchemaAdapter, BitrixSchemasAdapter
from .._base_entity import BaseEntity


class Field(BaseEntity):
    """Retrieve REST API v3 field descriptions as V3Field schemas.

    Raw result envelopes remain available through ``result``. Adapted ``value``
    and ``values`` unwrap ``item`` and ``items`` respectively. An explicit
    ``select`` must include all V3Field attributes when using adapted access;
    use raw ``result`` when requesting only part of a field description.

    Documentation: https://apidocs.bitrix24.com/api-reference/rest-v3.html#openapi
    """

    @type_checker
    def get(
            self,
            name: Text,
            *,
            select: Iterable[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIValueRequest[V3FieldGetData, V3Field]:
        """Get field description

        The method returns the description of the entity field by name.

        Args:
            name: The name of the field to retrieve;

            select: List of fields to return;

            timeout: Timeout in seconds.

        Returns:
            Lazy request exposing raw ``result.item`` and an adapted
            ``V3Field`` through ``value``.
        """

        params: JSONDict = {
            "name": name,
        }

        if select is not MISSING:
            if not isinstance(select, list):
                select = list(select)

            params["select"] = select

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValueRequest,
            result_adapter=BitrixSchemaAdapter(V3Field, wrapper="item"),
        )

    @type_checker
    def list(
            self,
            *,
            select: Iterable[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIValuesRequest[V3FieldListData, V3Field]:
        """Get a list of fields

        The method returns a list of available fields for the entity.

        Args:
            select: List of fields to return;

            timeout: Timeout in seconds.

        Returns:
            Lazy request exposing raw ``result.items`` and adapted
            ``V3Field`` instances through ``values``.
        """

        params: JSONDict = {}

        if select is not MISSING:
            if not isinstance(select, list):
                select = list(select)

            params["select"] = select

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params or None,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValuesRequest,
            result_adapter=BitrixSchemasAdapter(V3Field, wrapper="items"),
        )
