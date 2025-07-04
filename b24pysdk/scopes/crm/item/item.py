from typing import TYPE_CHECKING, Iterable, Optional, Text

from ...._bitrix_api_request import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import B24Bool, JSONDict, Timeout
from ..base_crm import BaseCRM

if TYPE_CHECKING:
    from .delivery import Delivery
    from .details import Details
    from .payment import Payment
    from .productrow import Productrow


class Item(BaseCRM):
    """The methods provide capabilities for managing various CRM entities, such as leads, deals, contacts, companies, invoices, estimates, and SPA elements.
    They allow you to retrieve fields, add, update, delete, and get lists of elements.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/index.html
    """

    ENTITY_TYPE_ID: Optional[int] = None
    """Numeric Identifier of Type."""

    ENTITY_TYPE_NAME: Optional[Text] = None
    """Symbolic Code of Type."""

    ENTITY_TYPE_ABBR: Optional[Text] = None
    """Short Symbolic Code of Type."""

    USER_FIELD_ENTITY_ID: Optional[Text] = None
    """User Field Object Type."""

    @type_checker
    def fields(
            self,
            *,
            entity_type_id: int,
            use_original_uf_names: bool = False,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get fields of CRM item.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/crm-item-fields.html

        This method retrieves a list of fields and their configuration for items of type entityTypeId.

        Args:
            entity_type_id: Identifier of the system or custom type whose element we want to retrieve;

            use_original_uf_names: This parameter controls the format of custom field names in the response;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "entityTypeId": entity_type_id,
            "useOriginalUfNames": str(B24Bool(use_original_uf_names)),
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.fields),
            params=params,
            timeout=timeout,
        )

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            entity_type_id: int,
            use_original_uf_names: bool = False,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create a new CRM entity.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/crm-item-add.html

        This method is a universal way to create objects in CRM. With it, you can create various types of objects, such as deals, contacts, companies, and more.

        To create an object, you need to pass the appropriate parameters, including the object type and its information: name, description, contact details, and other specifics.

        Upon successful execution of the request, a new object is created.

        Args:
            fields: Object format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
                };

            entity_type_id: Identifier of the system or user-defined type whose element we want to create;

            use_original_uf_names: This parameter controls the format of custom field names in the response;

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

    def _add(
            self,
            fields: JSONDict,
            *,
            entity_type_id: Optional[int] = None,
            use_original_uf_names: bool = False,
            params: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create a new CRM entity.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/crm-item-add.html

        This method is a universal way to create objects in CRM. With it, you can create various types of objects, such as deals, contacts, companies, and more.

        To create an object, you need to pass the appropriate parameters, including the object type and its information: name, description, contact details, and other specifics.

        Upon successful execution of the request, a new object is created.

        Args:
            fields: Object format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
                };

            entity_type_id: Identifier of the system or user-defined type whose element we want to create;

            use_original_uf_names: This parameter controls the format of custom field names in the response;

            params: Set of additional parameters where

                - REGISTER_SONET_EVENT - whether to register the change event in the activity stream 'Y' or not 'N',

                - IMPORT - whether an import mode enabled 'Y' or not 'N' (by default);

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "fields": fields,
            "entityTypeId": entity_type_id,
            "useOriginalUfNames": str(B24Bool(use_original_uf_names)),
            "params": params or dict(),
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.add),
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            entity_type_id: int,
            use_original_uf_names: bool = False,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Get an item by ID.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/crm-item-get.html

        The method returns information about an item based on the item identifier and the CRM object type identifier.

        Args:
            bitrix_id: Identifier of the item whose information we want to obtain;

            entity_type_id: Identifier of the system or user-defined type whose item we want to retrieve;

            use_original_uf_names: This parameter is used to control the format of custom field names in the response;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "entityTypeId": entity_type_id,
            "id": bitrix_id,
            "useOriginalUfNames": str(B24Bool(use_original_uf_names)),
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.get),
            params=params,
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
            use_original_uf_names: bool = False,
            timeout: Optional[int] = None,
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

            use_original_uf_names: This parameter controls the format of user field names in the request and response;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "entityTypeId": entity_type_id,
            "start": start,
            "useOriginalUfNames": str(B24Bool(use_original_uf_names)),
        }

        if select is not None:
            params["select"] = list(select)

        if filter is not None:
            params["filter"] = filter

        if order is not None:
            params["order"] = order

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.list),
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            entity_type_id: int,
            use_original_uf_names: bool = False,
            timeout: Optional[int] = None,
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

            use_original_uf_names: Parameter to control the format of custom field names in the request and response;

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

    def _update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            entity_type_id: Optional[int] = None,
            use_original_uf_names: bool = False,
            params: Optional[JSONDict] = None,
            timeout: Optional[int] = None,
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

            use_original_uf_names: Parameter to control the format of custom field names in the request and response;

            params: Set of additional parameters where

                - REGISTER_SONET_EVENT - whether to register the change event in the activity stream 'Y' or not 'N',

                - REGISTER_HISTORY_EVENT - whether to create a record on history 'Y' or not 'N';

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "entityTypeId": entity_type_id,
            "id": bitrix_id,
            "fields": fields,
            "useOriginalUfNames": str(B24Bool(use_original_uf_names)),
            "params": params or dict(),
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.update),
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            entity_type_id: int,
            timeout: Optional[int] = None,
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

        params = {
            "entityTypeId": entity_type_id,
            "id": bitrix_id,
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.delete),
            params=params,
            timeout=timeout,
        )

    @type_checker
    def import_(
            self,
            fields: JSONDict,
            *,
            entity_type_id: int,
            use_original_uf_names: bool = False,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "entityTypeId": entity_type_id,
            "fields": fields,
            "useOriginalUfNames": str(B24Bool(use_original_uf_names)),
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.import_),
            params=params,
            timeout=timeout,
        )

    @type_checker
    def batch_import(
            self,
            data: Iterable[JSONDict],
            *,
            entity_type_id: int,
            use_original_uf_names: bool = False,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "entityTypeId": entity_type_id,
            "data": list(data),
            "useOriginalUfNames": str(B24Bool(use_original_uf_names)),
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.batch_import),
            params=params,
            timeout=timeout,
        )

    @property
    def delivery(self) -> "Delivery":
        """"""
        from .delivery import Delivery

        if type(self) is __class__:
            return Delivery(self)
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no property delivery. Use 'Item' object instead!")

    @property
    def details(self) -> "Details":
        """"""
        from .details import Details

        if type(self) is __class__:
            return Details(self)
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no property details. Use 'Item' object instead!")

    @property
    def payment(self) -> "Payment":
        """"""
        from .payment import Payment

        if type(self) is __class__:
            return Payment(self)
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no property payment. Use 'Item' object instead!")

    @property
    def productrow(self) -> "Productrow":
        """"""
        from .productrow import Productrow

        if type(self) is __class__:
            return Productrow(self)
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no property productrow. Use 'Item' object instead!")
