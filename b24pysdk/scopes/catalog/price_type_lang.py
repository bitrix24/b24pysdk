from typing import Iterable, Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import classproperty, type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "PriceTypeLang",
]


class PriceTypeLang(BaseEntity):
    """Handle operations related to Bitrix24 catalog price type name translations.

    Documentation: https://apidocs.bitrix24.com/api-reference/catalog/price-type/price-type-lang/index.html
    """

    @classproperty
    def _name(cls) -> Text:
        return "priceTypeLang"

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create a new translation of a price type name.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/price-type/price-type-lang/catalog-price-type-lang-add.html

        This method adds a new translation for the price type name.

        Args:
            fields: Object format:
                {
                    "catalogGroupId": <catalog_price_type.id>,

                    "lang": <catalog_language.lid>,

                    "name": <string>,
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
        """Delete a translation of a price type name by its identifier.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/price-type/price-type-lang/catalog-price-type-lang-delete.html

        This method deletes the translation of the price type name by its identifier.

        Args:
            bitrix_id: Identifier of the price type name translation;

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
        """Retrieve a translation of a price type name by its identifier.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/price-type/price-type-lang/catalog-price-type-lang-get.html

        The method returns information about the translation of the price type name by its identifier.

        Args:
            bitrix_id: Identifier of the price type name translation;

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
        """Fetch a description of fields for the price type name translation object.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/price-type/price-type-lang/catalog-price-type-lang-get-fields.html

        This method returns the fields for translating the price type name.

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
    def get_languages(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve the list of available languages for translations.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/price-type/price-type-lang/catalog-price-type-lang-get-languages.html

        This method returns a list of available languages for translation.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.get_languages,
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
        """List translations of price type names by filter.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/price-type/price-type-lang/catalog-price-type-lang-list.html

        The method returns a list of translations for price type names.

        Args:
            select: List of fields to select. If omitted or empty, all available fields are selected;

            filter: Object format:
                {
                    "field_1": "value_1",

                    ...,

                    "field_N": "value_N",
                }
                where possible keys correspond to catalog_price_type_lang fields;

            order: Object format:
                {
                    field_1: value_1,

                    ...,
                }

                where

                - field_n is the field name to sort by;

                - value_n is 'ASC' for ascending or 'DESC' for descending;

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
        """Update a translation of a price type name by its identifier.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/price-type/price-type-lang/catalog-price-type-lang-update.html

        This method updates the translation of the price type name by its identifier.

        Args:
            bitrix_id: Identifier of the price type name translation;

            fields: Object format:
                {
                    "catalogGroupId": <catalog_price_type.id>,

                    "lang": <catalog_language.lid>,

                    "name": <string>,
                };

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
