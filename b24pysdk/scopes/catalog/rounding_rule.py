from typing import Iterable, Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import classproperty, type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "RoundingRule",
]


class RoundingRule(BaseEntity):
    """Handle price rounding rules in trade catalog.

    Documentation: https://apidocs.bitrix24.com/api-reference/catalog/rounding-rule/index.html
    """

    @classproperty
    def _name(cls) -> Text:
        return "roundingRule"

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create a price rounding rule

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/rounding-rule/catalog-rounding-rule-add.html

        This method adds a price rounding rule.

        Args:
            fields: Field values for creating a new price rounding rule;

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
        """Delete a price rounding rule

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/rounding-rule/catalog-rounding-rule-delete.html

        This method deletes a price rounding rule.

        Args:
            bitrix_id: Identifier of the price rounding rule;

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
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get values of the price rounding rule fields

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/rounding-rule/catalog-rounding-rule-get.html

        The method returns information about the price rounding rule by its identifier.

        Args:
            bitrix_id: Identifier of the price rounding rule;

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
        """Get fields of the price rounding rule

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/rounding-rule/catalog-rounding-rule-get-fields.html

        The method returns the fields of the price rounding rule.

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
        """Get a list of price rounding rules by filter

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/rounding-rule/catalog-rounding-rule-list.html

        The method returns a list of price rounding rules.

        Args:
            select: An array with the list of fields to select;

             filter: Object format:
                {
                    "field_1": "value_1",

                    ...,

                    "field_N": "value_N",
                }
                where possible values for field correspond to the fields of the catalog rounding rule;

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
        """Update price rounding rule

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/rounding-rule/catalog-rounding-rule-update.html

        Args:
            bitrix_id: Identifier of the price rounding rule;

            fields: Field values for updating a new price rounding rule;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "id": bitrix_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
