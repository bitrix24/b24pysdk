from typing import Iterable, Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Measure",
]


class Measure(BaseEntity):
    """Handle operations related to Bitrix24 catalog measures.

    Documentation: https://apidocs.bitrix24.com/api-reference/catalog/measure/
    """

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create a new unit of measurement.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/measure/catalog-measure-add.html

        Args:
            fields: Object format:
                {
                    "code": integer,

                    "isDefault": "Y" | "N",

                    "measureTitle": string,

                    "symbol": string,

                    "symbolIntl": string,

                    "symbolLetterIntl": string,
                };

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest."""

        params: JSONDict = {
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete a unit of measurement by its identifier.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/measure/catalog-measure-delete.html

        Args:
            bitrix_id: Identifier of the measure;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest."""

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Retrieve information about a unit of measurement by its identifier.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/measure/catalog-measure-get.html

        Args:
            bitrix_id: Identifier of the measure;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest."""

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
        """Retrieve the list of available fields for the measure entity.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/measure/catalog-measure-get-fields.html

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
            select: Optional[Iterable[Text]] = None,
            filter: Optional[JSONDict] = None,
            order: Optional[JSONDict] = None,
            start: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Retrieve a list of units of measurement.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/measure/catalog-measure-list.html

        The method returns a list of measurement units.

        Args:
            select: Iterable of field names to select. If omitted or empty, all available fields are returned;

            filter: Object format:
                {
                    "field_1": "value_1",

                    ...,

                    "field_N": "value_N",
                };
                where keys correspond to the catalog_measure fields;

            order: Optional sorting options;

            start: Optional numeric value controlling the starting position;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest."""

        params: JSONDict = dict()

        if select is not None:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        if filter is not None:
            params["filter"] = filter

        if order is not None:
            params["order"] = order

        if start is not None:
            params["start"] = start


        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update an existing unit of measurement.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/measure/catalog-measure-update.html

        Args:
            bitrix_id: Identifier of the measure;

            fields: Object format:
                {
                    "code": integer,

                    "isDefault": "Y" | "N",

                    "measureTitle": string,

                    "symbol": string,

                    "symbolIntl": string,

                    "symbolLetterIntl": string,
                };

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest."""

        params: JSONDict = {
            "id": bitrix_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
