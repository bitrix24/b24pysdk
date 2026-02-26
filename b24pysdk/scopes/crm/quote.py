from functools import cached_property
from typing import Iterable, Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from ._productrows import Productrows
from ._userfield import Userfield
from .item.base_item import BaseItem

__all__ = [
    "Quote",
]


class Quote(BaseItem):
    """An estimate is a CRM object that allows you to create printed documents and send them to the client before a deal.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/quote/index.html
    """

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
        """Get fields of the estimate.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/quote/crm-quote-fields.html

        The method returns the description of fields for the estimate including custom fields.

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
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create a new estimate.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/quote/crm-quote-add.html

        The method creates a new estimate.

        The created estimate must include the seller and buyer companies.

        Args:
            fields: Object format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
                }

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._add(fields, timeout=timeout)

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get an estimate by ID.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/quote/crm-quote-get.html

        The method returns an estimate by its ID.

        Args:
            bitrix_id: Identifier of the estimate;

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
        """Get list of estimates.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/quote/crm-quote-list.html

        The method returns a list of estimates by filter.

        Args:
            select: List of fields that should be populated for deals in the selection;

            filter: Object format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
                }

            order:  Object format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
                }

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
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update the estimate.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/quote/crm-quote-update.html

        The method updates an existing estimate.

        Args:
            bitrix_id: Identifier of the estimate;

            fields: Object format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
                }

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._update(
            bitrix_id,
            fields,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete estimate.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/quote/crm-quote-delete.html

        The method removes an estimate and all associated objects.

        Args:
            bitrix_id: Identifier of the estimate;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._delete(bitrix_id, timeout=timeout)
