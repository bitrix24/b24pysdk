from abc import ABC
from typing import Iterable, Optional, Text, Union

from ....api.requests import BitrixAPIRequest
from ....utils.types import B24BoolStrict, JSONDict, Timeout
from .._base_crm import BaseCRM


class BaseItem(BaseCRM, ABC):
    """The methods provide capabilities for managing various CRM entities, such as leads, deals, contacts, companies, invoices, estimates, and SPA elements.
    They allow you to retrieve fields, add, update, delete, and get lists of elements.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/index.html
    """

    def _fields(
            self,
            *,
            entity_type_id: Optional[int] = None,
            use_original_uf_names: Optional[Union[bool, B24BoolStrict]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get fields of CRM item.

        This method retrieves a list of fields and their configuration for items of type entityTypeId.

        Args:
            entity_type_id: Identifier of the system or custom type whose element we want to retrieve;

            use_original_uf_names: This parameter controls the format of custom field names in the responses;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict()

        if entity_type_id is not None:
            params["entityTypeId"] = entity_type_id

        if use_original_uf_names is not None:
            params["originalUfNames"] = B24BoolStrict(use_original_uf_names).to_b24()

        return self._make_bitrix_api_request(
            api_wrapper=self._fields,
            params=params,
            timeout=timeout,
        )

    def _add(
            self,
            fields: JSONDict,
            *,
            entity_type_id: Optional[int] = None,
            use_original_uf_names: Optional[Union[bool, B24BoolStrict]] = None,
            extra_params: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create a new CRM entity.

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

            extra_params: Set of additional parameters where

                - REGISTER_SONET_EVENT - whether to register the change event in the activity stream 'Y' or not 'N',

                - IMPORT - whether an import mode enabled 'Y' or not 'N' (by default);

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "fields": fields,
        }

        if entity_type_id is not None:
            params["entityTypeId"] = entity_type_id

        if use_original_uf_names is not None:
            params["useOriginalUfNames"] = B24BoolStrict(use_original_uf_names).to_b24()

        if extra_params is not None:
            params["params"] = extra_params

        return self._make_bitrix_api_request(
            api_wrapper=self._add,
            params=params,
            timeout=timeout,
        )

    def _get(
            self,
            bitrix_id: int,
            *,
            entity_type_id: Optional[int] = None,
            use_original_uf_names: Optional[Union[bool, B24BoolStrict]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get an item by ID.

        The method returns information about an item based on the item identifier and the CRM object type identifier.

        Args:
            bitrix_id: Identifier of the item whose information we want to obtain;

            entity_type_id: Identifier of the system or user-defined type whose item we want to retrieve;

            use_original_uf_names: This parameter is used to control the format of custom field names in the responses;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
        }

        if entity_type_id is not None:
            params["entityTypeId"] = entity_type_id

        if use_original_uf_names is not None:
            params["useOriginalUfNames"] = B24BoolStrict(use_original_uf_names).to_b24()

        return self._make_bitrix_api_request(
            api_wrapper=self._get,
            params=params,
            timeout=timeout,
        )

    def _list(
            self,
            *,
            entity_type_id: Optional[int] = None,
            select: Optional[Iterable[Text]] = None,
            filter: Optional[JSONDict] = None,
            order: Optional[JSONDict] = None,
            start: Optional[int] = None,
            use_original_uf_names: Optional[Union[bool, B24BoolStrict]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of CRM elements.

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

        params = dict()

        if entity_type_id is not None:
            params["entityTypeId"] = entity_type_id

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

        if use_original_uf_names is not None:
            params["useOriginalUfNames"] = B24BoolStrict(use_original_uf_names).to_b24()

        return self._make_bitrix_api_request(
            api_wrapper=self._list,
            params=params,
            timeout=timeout,
        )

    def _update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            entity_type_id: Optional[int] = None,
            use_original_uf_names: Optional[Union[bool, B24BoolStrict]] = None,
            extra_params: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update CRM item.

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

            extra_params: Set of additional parameters where

                - REGISTER_SONET_EVENT - whether to register the change event in the activity stream 'Y' or not 'N',

                - REGISTER_HISTORY_EVENT - whether to create a record on history 'Y' or not 'N';

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
            "fields": fields,
        }

        if entity_type_id is not None:
            params["entityTypeId"] = entity_type_id

        if use_original_uf_names is not None:
            params["useOriginalUfNames"] = B24BoolStrict(use_original_uf_names).to_b24()

        if extra_params is not None:
            params["params"] = extra_params

        return self._make_bitrix_api_request(
            api_wrapper=self._update,
            params=params,
            timeout=timeout,
        )

    def _delete(
            self,
            bitrix_id: int,
            *,
            entity_type_id: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete CRM item.

        This method deletes a CRM entity item by its item ID and entity type ID.

        Args:
            bitrix_id: The ID of the item to be deleted;

            entity_type_id: The ID of the system or user-defined type of the item we want to delete;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
        }

        if entity_type_id is not None:
            params["entityTypeId"] = entity_type_id

        return self._make_bitrix_api_request(
            api_wrapper=self._delete,
            params=params,
            timeout=timeout,
        )
