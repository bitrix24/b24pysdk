from typing import Iterable, Optional, Text

from ...._bitrix_api_request import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict

from ..base_crm import BaseCRM
from .item import Item


class Productrow(BaseCRM):
    """The methods allow you to work with product items associated with various CRM objects.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/product-rows/index.html
    """

    def __init__(self, item: Item):
        super().__init__(item._scope)
        self._path = self._get_path(item)

    def fields(
            self,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Get fields for the product rows.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/product-rows/crm-item-productrow-fields.html

        This method retrieves a list of fields for product rows.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return self._fields(timeout=timeout)

    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Add product item.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/product-rows/crm-item-productrow-add.html

        This method adds a product item to a CRM object.

        Args:
            fields: Object in the format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
                };

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._add(fields, timeout=timeout)

    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Get product by ID.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/product-rows/crm-item-productrow-get.html

        The method retrieves information about a product item in the CRM.

        Args:
            bitrix_id: Identifier of the company;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._get(bitrix_id, timeout=timeout)

    def list(
            self,
            *args,
            filter: Optional[JSONDict] = None,
            order: Optional[JSONDict] = None,
            start: Optional[int] = None,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Get a list of product rows.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/product-rows/crm-item-productrow-list.html

        The method retrieves product rows of the CRM object.

        Args:
            filter: Object in the format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
                };

            order: Object format:

                {
                    field_1: value_1,

                    ...,
                }

                where

                - field_n is the name of the field by which the selection will be sorted

                - value_n is a string value equals to 'asc' (ascending sort) or 'desc' (descending sort);

            start: This parameter is used to manage pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._list(
            filter=filter,
            order=order,
            start=start,
            timeout=timeout,
        )

    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Update product row.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/product-rows/crm-item-productrow-update.html

        This method updates the product row of a CRM object.

        Args:
            bitrix_id: Identifier of the product row;

            fields: Object in the format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
                };

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._update(bitrix_id, fields, timeout=timeout)

    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Delete product row.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/product-rows/crm-item-productrow-delete.html

        This method removes a product row from the CRM object.

        Args:
            bitrix_id: Identifier of the product row;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._delete(bitrix_id, timeout=timeout)

    @type_checker
    def set(
            self,
            *,
            owner_id: int,
            owner_type: Text,
            product_rows: Iterable[JSONDict],
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Save product row.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/product-rows/crm-item-productrow-set.html

        This method saves the product row of a CRM object. This method will overwrite all existing product rows associated with the object.

        Args:
            owner_id: Identifier of the CRM object;

            owner_type: Identifier of the CRM object type;

            product_rows: Array of objects containing information about the product rows to be saved in the object;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "ownerId": owner_id,
            "ownerType": owner_type,
            "product_rows": list(product_rows),
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.set),
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_available_for_payment(
            self,
            *,
            owner_id: int,
            owner_type: Text,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Get unpaid product items.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/product-rows/crm-item-productrow-get-available-for-payment.html

        The method retrieves product items of the CRM object for which the client has not yet been billed.

        Args:
            owner_id: Identifier of the CRM object;

            owner_type: Identifier of the CRM object type;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "ownerId": owner_id,
            "ownerType": owner_type,
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.get_available_for_payment),
            params=params,
            timeout=timeout,
        )
