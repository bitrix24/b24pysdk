from typing import Iterable, Optional, Text

from ...bitrix_api.classes import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from ._userfield import Userfield
from .details.details import Details
from .item.base_item import BaseItem
from .relationships import Company


class Contact(BaseItem):
    """The methods provide capabilities for managing contacts.
    They allow you to retrieve fields, add, update, delete, and get lists of contacts.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/contacts/index.html
    """

    ENTITY_TYPE_ID = 3
    ENTITY_TYPE_NAME = "CONTACT"
    ENTITY_TYPE_ABBR = "C"
    USER_FIELD_ENTITY_ID = "CRM_CONTACT"

    @property
    def company(self) -> Company:
        """"""
        return Company(self)

    @property
    def details(self) -> "Details":
        """"""
        return Details(self)

    @property
    def userfield(self) -> Userfield:
        """"""
        return Userfield(self)

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get contact fields.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/contacts/crm-contact-fields.html

        The method returns the description of contact fields, including custom fields.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._fields(timeout=timeout)

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            params: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create a new contact.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/contacts/crm-contact-add.html

        The method create a new contact.

        Args:
            fields: Object format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
                };

            params: An objects containing a set of additional parameters where

                - REGISTER_SONET_EVENT - whether to register the change event in the activity stream 'Y' or not 'N',

                - IMPORT - whether an import mode enabled 'Y' or not 'N' (by default);

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return super()._add(
            fields,
            extra_params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get contact by ID.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/contacts/crm-contact-get.html

        The method returns a contact by its identifier.

        Args:
            bitrix_id: Identifier of the contact;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._get(bitrix_id, timeout=timeout)

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
        """Get a list of contacts.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/contacts/crm-contact-list.html

        The method returns a list of contacts based on a filter.

        Args:
            select: List of fields that should be populated in the selected elements;

            filter: Object in the format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
                }

            order: Object format:

                {
                    field_1: value_1,

                    ...,
                }

                where

                - field_n is the name of the field by which the selection will be sorted

                - value_n is a string value equals to 'ASC' (ascending sort) or 'DESC' (descending sort);

            start: This parameter is used to manage pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._list(
            select=select,
            filter=filter,
            order=order,
            start=start,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            params: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update contact.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/contacts/crm-contact-update.html

        The method updates an existing contact.

        Args:
            bitrix_id: Identifier of the contact to be changed;

            fields: Object in the format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
                }

            params: Set of additional parameters where

                - REGISTER_SONET_EVENT - whether to register the change event in the activity stream 'Y' or not 'N',

                - REGISTER_HISTORY_EVENT - whether to create a record in history 'Y' or not 'N';

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._update(
            bitrix_id,
            fields,
            extra_params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete contact.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/contacts/crm-contact-delete.html

        The method removes a contact and all associated objects.

        Args:
            bitrix_id: Identifier of the contact;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._delete(bitrix_id, timeout=timeout)
