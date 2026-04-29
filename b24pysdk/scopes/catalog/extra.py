from typing import Iterable, Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Extra",
]


class Extra(BaseEntity):
    """Handle operations related to Bitrix24 catalog extras.

    Documentation: https://apidocs.bitrix24.com/api-reference/catalog/extra/index.html
    """

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Retrieve information about a specific catalog extra by its identifier.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/extra/catalog-extra-get.html

        This method returns details of the extra markup with the specified identifier.

        Args:
            bitrix_id: Identifier of the extra markup in Bitrix24;

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
        """Retrieve field descriptions for the catalog extra entity.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/extra/catalog-extra-get-fields.html

        Returns a map of field identifiers to their descriptions.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest."""
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
        """Retrieve a list of catalog extras by filter.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/extra/catalog-extra-list.html

        Use select to limit returned fields, filter to constrain results, order to sort, and start for pagination.

        Args:
            select: Fields to be selected. If omitted or empty, all available fields are returned;

            filter: Object format:
                {
                    "field_1": "value_1",

                    ...,

                    "field_N": "value_N",

                }, where the key may include a prefix to refine filtering behavior;

            order: Object format:
                {
                    field_1: value_1,

                    ...,

                }
                where

                - field_n is the name of the field by which the selection will be sorted

                - value_n is a string value equals to 'ASC' (ascending sort) or 'DESC' (descending sort);

            start: Value to start the selection from for paginated output;

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
