from typing import Iterable, Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Ratio",
]


class Ratio(BaseEntity):
    """
    Handle measurements unit ratios in the trade catalog.

    Documentation: https://apidocs.bitrix24.com/api-reference/catalog/ratio/index.html
    """

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get unit of measure Ratio field values

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/ratio/catalog-ratio-get.html

        The method returns the values of the unit of measure ratio fields by identifier.

        Args:
            bitrix_id: Identifier of the unit of measure ratio;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get Measurement Unit Ratio Fields

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/ratio/catalog-ratio-get-fields.html

        The method returns the available fields of the measurement unit ratio.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.get_fields,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            select: Optional[Iterable[Text]] = MISSING,
            filter: Optional[JSONDict] = MISSING,
            order: Optional[JSONDict] = MISSING,
            start: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of measurement unit ratios

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/ratio/catalog-ratio-list.html

        The method returns a list of measurement unit ratios.

        Args:
            select: An array with the list of fields to select;

             filter: Object format:
                {
                    "field_1": "value_1",

                    ...,

                    "field_N": "value_N",
                }
                where possible values for field correspond to the fields of the catalog ratio object;

            order: Object format:
                {
                    field_1: value_1,

                    ...,
                }

                where

                - field_n is the field name to sort by;

                - value_n is 'asc' for ascending or 'desc' for descending;

            start: Starting position for pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {}

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        if filter is not MISSING:
            params["filter"] = filter

        if order is not MISSING:
            params["order"] = order

        if start is not MISSING:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
