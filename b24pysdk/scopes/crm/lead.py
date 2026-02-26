from functools import cached_property
from typing import Iterable, Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from ._productrows import Productrows
from ._relationships import Contact
from ._userfield import Userfield
from .details import Details
from .item.base_item import BaseItem

__all__ = [
    "Lead",
]


class Lead(BaseItem):
    """The methods provide capabilities for managing leads.
    They allow you to retrieve fields, add, update, delete, and get lists of leads.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/leads/index.html
    """

    @cached_property
    def contact(self) -> Contact:
        """"""
        return Contact(self)

    @cached_property
    def details(self) -> Details:
        """"""
        return Details(self)

    @cached_property
    def productrows(self) -> Productrows:
        """"""
        return Productrows(self)

    @cached_property
    def userfield(self) -> Userfield:
        """"""
        return Userfield(self)

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get CRM lead fields.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/leads/crm-lead-fields.html

        The method returns the description of lead fields, including custom fields.

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
        """Create a new lead.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/leads/crm-lead-add.html

        The method creates a new lead.

        Args:
            fields: Object format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
                };

            params: Set of additional parameters where

                - REGISTER_SONET_EVENT - whether to register additional event 'Y' or not 'N',

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return self._add(
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
        """Get lead by ID.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/leads/crm-lead-get.html

        The method returns a lead by its identifier.

        Args:
            bitrix_id: The identifier of the lead;

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
        """Get a list of leads.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/leads/crm-lead-list.html

        The method returns a list of leads based on a filter.

        Args:
            select: An array containing the list of fields to be selected;

            filter: Object format:

                {
                    "field_1": "value_1",

                    "field_2": "value_2",

                    ...,

                    "field_n": "value_n",
                }

            order: Object format:

                {
                    field_1: value_1,

                    ...,
                }

                where

                - field_n is the name of the field by which the selection will be sorted

                - value_n is a string value equals to 'asc' (ascending sort) or 'desc' (descending sort);

            start: This parameter is used to control pagination;

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
        """Update lead.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/leads/crm-lead-update.html

        The method updates an existing lead.

        Args:
            bitrix_id: lead identifier;

            fields: Object format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
                }

            params: Set of additional parameters where

                - REGISTER_SONET_EVENT - whether to register the change event in the activity stream 'Y' or not 'N';

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
        """Delete lead.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/leads/crm-lead-delete.html

        The method removes a lead and all associated objects: tasks, history, timeline records, and others.

        Objects are deleted if they are not linked to other objects or entities. If the objects are linked to other entities, only the link to the deleted lead will be removed.

        Args:
            bitrix_id: Identifier of the lead;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._delete(bitrix_id, timeout=timeout)
