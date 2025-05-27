from typing import Iterable, Optional, Text

from ..._bitrix_api_request import BitrixAPIRequest
from ...utils.types import JSONDict

from .item import Item
from .relationships import Company
from ._userfield import Userfield


class Contact(Item):
    """The methods provide capabilities for managing contacts.
    They allow you to retrieve fields, add, update, delete, and get lists of contacts.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/contacts/index.html
    """

    ENTITY_TYPE_ID = 3
    ENTITY_TYPE_NAME = "CONTACT"
    ENTITY_TYPE_ABBR = "C"
    USER_FIELD_ENTITY_ID = "CRM_CONTACT"

    def fields(
            self,
            *args,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Get contact fields.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/contacts/crm-contact-fields.html

        The method returns the description of contact fields, including custom fields.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return super().fields(entity_type_id=self.ENTITY_TYPE_ID, timeout=timeout)

    def add(
            self,
            fields: JSONDict,
            *args,
            params: Optional[JSONDict] = None,
            timeout: Optional[int] = None,
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
            entity_type_id=self.ENTITY_TYPE_ID,
            params=params,
            timeout=timeout,
        )

    def get(
            self,
            bitrix_id: int,
            *args,
            timeout: Optional[int] = None,
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
        return super().get(
            bitrix_id,
            entity_type_id=self.ENTITY_TYPE_ID,
            timeout=timeout,
        )

    def list(
            self,
            *args,
            select: Optional[Iterable[Text]] = None,
            filter: Optional[JSONDict] = None,
            order: Optional[JSONDict] = None,
            start: Optional[int] = None,
            timeout: Optional[int] = None,
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
        return super().list(
            entity_type_id=self.ENTITY_TYPE_ID,
            select=select,
            filter=filter,
            order=order,
            start=start,
            timeout=timeout,
        )

    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *args,
            params: Optional[JSONDict] = None,
            timeout: Optional[int] = None,
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
        return super()._update(
            bitrix_id,
            fields,
            entity_type_id=self.ENTITY_TYPE_ID,
            params=params,
            timeout=timeout,
        )

    def delete(
            self,
            bitrix_id: int,
            *args,
            timeout: Optional[int] = None,
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
        return super().delete(
            bitrix_id,
            entity_type_id=self.ENTITY_TYPE_ID,
            timeout=timeout,
        )

    @property
    def company(self) -> Company:
        """"""
        return Company(self)

    @property
    def userfield(self) -> Userfield:
        """"""
        return Userfield(self)
