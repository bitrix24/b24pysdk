from typing import Iterable, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity


class Field(BaseEntity):
    """Base class for retrieving entity fields.

    Documentation: https://apidocs.bitrix24.com/api-reference/rest-v3.html#openapi
    """

    @type_checker
    def get(
            self,
            name: Text,
            *,
            select: Iterable[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get field description

        The method returns the description of the entity field by name.

        Args:
            name: The name of the field to retrieve;

            select: List of fields to return;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
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
        )

    @type_checker
    def list(
            self,
            *,
            select: Iterable[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of fields

        The method returns a list of available fields for the entity.

        Args:
            select: List of fields to return;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
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
        )
