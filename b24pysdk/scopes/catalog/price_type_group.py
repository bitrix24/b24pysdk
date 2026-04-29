from typing import Iterable, Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import classproperty, type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "PriceTypeGroup",
]


class PriceTypeGroup(BaseEntity):
    """Handle operations related to Bitrix24 catalog price type group bindings.

    Documentation: https://apidocs.bitrix24.com/api-reference/catalog/price-type/price-type-group/
    """

    @classproperty
    def _name(cls) -> Text:
        return "priceTypeGroup"

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create a binding between a price type and a customer group.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/price-type/price-type-group/catalog-price-type-group-add.html

        The method adds a price type binding to a customer group.

        Args:
            fields: Object format:
                {
                    "catalogGroupId": value,

                    "groupId": value,

                    "access": value,
                };

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

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
        """Delete a binding between a price type and a customer group by identifier.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/price-type/price-type-group/catalog-price-type-group-delete.html

        The method removes the binding of a price type to a customer group by its identifier.

        Args:
            bitrix_id: Identifier of the price type group binding;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Retrieve a description of fields for price type group bindings.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/price-type/price-type-group/catalog-price-type-group-get-fields.html

        The method returns the description of the fields binding price types to customer groups.

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
        """Retrieve a list of bindings between price types and customer groups

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/price-type/price-type-group/catalog-price-type-group-list.html

        The method returns a list of price type bindings to customer groups.

        Args:
            select: Iterable with the list of catalog_price_type_group fields to select. If not provided or empty, all available fields are returned;

            filter: Object format:
                {
                    "field_1": "value_1",

                    ...,

                    "field_N": "value_N",
                }
                where field names correspond to catalog_price_type_group fields;

            order: Object format:
                {
                    field_1: direction_1,

                    ...,
                }
                where direction is a string value such as 'ASC' or 'DESC';

            start: Start position for selection (used for navigation);

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

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
