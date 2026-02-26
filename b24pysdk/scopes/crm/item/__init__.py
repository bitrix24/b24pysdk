from functools import cached_property
from typing import Iterable, Optional, Text, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import B24BoolStrict, JSONDict, Timeout
from .base_item import BaseItem
from .delivery import Delivery
from .details import Details
from .payment import Payment
from .productrow import Productrow

__all__ = [
    "Item",
]


class Item(BaseItem):
    """The methods provide capabilities for managing various CRM entities, such as leads, deals, contacts, companies, invoices, estimates, and SPA elements.
    They allow you to retrieve fields, add, update, delete, and get lists of elements.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/index.html
    """

    @cached_property
    def delivery(self) -> "Delivery":
        """"""
        return Delivery(self)

    @cached_property
    def details(self) -> "Details":
        """"""
        return Details(self)

    @cached_property
    def payment(self) -> "Payment":
        """"""
        return Payment(self)

    @cached_property
    def productrow(self) -> "Productrow":
        """"""
        return Productrow(self)

    @type_checker
    def fields(
            self,
            *,
            entity_type_id: int,
            use_original_uf_names: Optional[bool] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get fields of CRM item.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/crm-item-fields.html

        This method retrieves a list of fields and their configuration for items of type entityTypeId.

        Args:
            entity_type_id: Identifier of the system or custom type whose element we want to retrieve;

            use_original_uf_names: This parameter controls the format of custom field names in the responses;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._fields(
            entity_type_id=entity_type_id,
            use_original_uf_names=use_original_uf_names,
            timeout=timeout,
        )

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            entity_type_id: int,
            use_original_uf_names: Optional[bool] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create a new CRM entity.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/crm-item-add.html

        This method is a universal way to create objects in CRM. With it, you can create various types of objects, such as deals, contacts, companies, and more.

        To create an object, you need to pass the appropriate parameters, including the object type and its information: name, description, contact details, and other specifics.

        Upon successful execution of the requests, a new object is created.

        Args:
            fields: Object format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
                };

            entity_type_id: Identifier of the system or user-defined type whose element we want to create;

            use_original_uf_names: This parameter controls the format of custom field names in the responses;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._add(
            fields,
            entity_type_id=entity_type_id,
            use_original_uf_names=use_original_uf_names,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            entity_type_id: int,
            use_original_uf_names: Optional[bool] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get an item by ID.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/crm-item-get.html

        The method returns information about an item based on the item identifier and the CRM object type identifier.

        Args:
            bitrix_id: Identifier of the item whose information we want to obtain;

            entity_type_id: Identifier of the system or user-defined type whose item we want to retrieve;

            use_original_uf_names: This parameter is used to control the format of custom field names in the responses;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._get(
            bitrix_id=bitrix_id,
            entity_type_id=entity_type_id,
            use_original_uf_names=use_original_uf_names,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            entity_type_id: int,
            select: Optional[Iterable[Text]] = None,
            filter: Optional[JSONDict] = None,
            order: Optional[JSONDict] = None,
            start: Optional[int] = None,
            use_original_uf_names: Optional[bool] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of CRM elements.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/crm-item-list.html

        This method retrieves a list of elements of a specific type of CRM entity.

        CRM entity elements will not be included in the final selection if the user does not have "read" access permission for these elements.

        Args:
            entity_type_id: Identifier of the system or user-defined type whose item we want to retrieve;

            select: List of fields that should be populated in the selected elements;

            filter: Object format:

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

                - value_n is a string value equals to 'ASC' (ascending sort) or 'DESC' (descending sort);

            start: This parameter is used to manage pagination;

            use_original_uf_names: This parameter controls the format of user field names in the requests and responses;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._list(
            entity_type_id=entity_type_id,
            select=select,
            filter=filter,
            order=order,
            start=start,
            use_original_uf_names=use_original_uf_names,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            entity_type_id: int,
            use_original_uf_names: Optional[bool] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update CRM item.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/crm-item-update.html

        This method updates an item of a specific type in the CRM object by assigning new values from the fields parameter.

        Args:
            bitrix_id: Identifier of the item we want to change;

            fields: Object format

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
                };

            entity_type_id: Identifier of the system or user-defined type whose item we want to change;

            use_original_uf_names: Parameter to control the format of custom field names in the requests and responses;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._update(
            bitrix_id,
            fields,
            entity_type_id=entity_type_id,
            use_original_uf_names=use_original_uf_names,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            entity_type_id: int,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete CRM item.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/crm-item-delete.html

        This method deletes a CRM entity item by its item ID and entity type ID.

        Args:
            bitrix_id: The ID of the item to be deleted;

            entity_type_id: The ID of the system or user-defined type of the item we want to delete;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._delete(
            bitrix_id=bitrix_id,
            entity_type_id=entity_type_id,
            timeout=timeout,
        )

    @type_checker
    def import_(
            self,
            fields: JSONDict,
            *,
            entity_type_id: int,
            use_original_uf_names: Optional[Union[bool, B24BoolStrict]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Import a single record

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/import/crm-item-import.html

        A universal method for importing objects into CRM.

        Args:
            fields: Object in the format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,

                }

                where:
                    field_n — field name

                    value_n — field value;

            entity_type_id: Identifier of the system or custom type for which the item needs to be created;

            use_original_uf_names: Parameter to control the format of custom field names in the requests and responses;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "entityTypeId": entity_type_id,
            "fields": fields,
        }

        if use_original_uf_names is not None:
            params["useOriginalUfNames"] = B24BoolStrict(use_original_uf_names).to_b24()

        return self._make_bitrix_api_request(
            api_wrapper=self.import_,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def batch_import(
            self,
            data: Iterable[JSONDict],
            *,
            entity_type_id: int,
            use_original_uf_names: Optional[Union[bool, B24BoolStrict]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Import a batch of CRM records.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/import/crm-item-batch-import.html

        A universal method for importing objects into CRM.

        Args:
            data: An array of fields values for the items;

            entity_type_id: Identifier of the system or custom type for which the item needs to be created;

            use_original_uf_names: Parameter to control the format of custom field names in the requests and responses;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if data.__class__ is not list:
            data = list(data)

        params = {
            "entityTypeId": entity_type_id,
            "data": data,
        }

        if use_original_uf_names is not None:
            params["useOriginalUfNames"] = B24BoolStrict(use_original_uf_names).to_b24()

        return self._make_bitrix_api_request(
            api_wrapper=self.batch_import,
            params=params,
            timeout=timeout,
        )
