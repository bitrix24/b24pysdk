from functools import cached_property
from typing import Iterable, Optional, Text

from ...bitrix_api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from ._relationships import Contact
from ._userfield import Userfield
from .details import Details
from .item.base_item import BaseItem

__all__ = [
    "Company",
]


class Company(BaseItem):
    """The methods provide capabilities for managing companies.
    They allow you to retrieve fields, add, update, delete, and get lists of companies.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/companies/index.html
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
    def userfield(self) -> Userfield:
        """"""
        return Userfield(self)

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get company fields.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/companies/crm-company-fields.html

        The method returns the description of company fields? including custom fields.

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
        """Create a new company.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/companies/crm-company-add.html

        The method create a new company.

        Args:
            fields: Object format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
                };

            params: An objects containing a set of additional parameters where

                - REGISTER_SONET_EVENT - whether to register the change event in the live feed 'Y' or not 'N'

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
        """Get company by ID.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/companies/crm-company-get.html

        The method returns a company by its identifier.

        Args:
            bitrix_id: Identifier of the company;

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
        """Get a list of companies.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/companies/crm-company-list.html

        The method returns a list of companies based on a filter.

        Args:
            select: List of fields that should be populated in the selected elements;

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
        """Update company.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/companies/crm-company-update.html

        The method updates an existing company.

        Args:
            bitrix_id: Identifier of the company to be changed;

            fields: Object in the format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
                };

            params: Set of additional parameters where

                - REGISTER_SONET_EVENT - whether to register the change event in the live feed 'Y' or not 'N';

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
        """Delete company.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/companies/crm-company-delete.html

        The method removes a contact and all associated objects.

        Args:
            bitrix_id: Identifier of the company;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._delete(bitrix_id, timeout=timeout)
