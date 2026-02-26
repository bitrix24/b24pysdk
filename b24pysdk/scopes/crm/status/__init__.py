from functools import cached_property
from typing import Optional

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from .._base_crm import BaseCRM
from .entity import Entity

__all__ = [
    "Status",
]


class Status(BaseCRM):
    """The methods provide capabilities for managing elements from the reference book.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/status/index.html
    """

    @cached_property
    def entity(self) -> Entity:
        """"""
        return Entity(self)

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get description of CRM status fields.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/status/crm-status-fields.html

        The method returns a description of the fields in the directory.

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
        """Create a new CRM directory element.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/status/crm-status-add.html

        The method creates a new element in the specified directory.

        Args:
            fields: Object format:

                {
                    "ENTITY_ID": "DEAL_STAGE",

                    "STATUS_ID": "DECISION",

                    "NAME": "Decision-Making",

                    "SORT": 70
                };

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._add(fields=fields, timeout=timeout)

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the directory item by ID.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/status/crm-status-get.html

        The method returns the directory item by ID.

        Args:
            bitrix_id:  Identifier of the directory item;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._get(bitrix_id=bitrix_id, timeout=timeout)

    @type_checker
    def list(
            self,
            *,
            filter: Optional[JSONDict] = None,
            order: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of directory items by filter.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/status/crm-status-list.html

        The  method returns a list of directory items on the filter.

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

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict()

        if filter is not None:
            params["filter"] = filter

        if order is not None:
            params["order"] = order

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
        """Update an existing CRM directory item.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/status/crm-status-update.html

        This method updates an existing directory item.

        Args:
            bitrix_id: Identifier of the directory item;

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
        return self._update(
            bitrix_id=bitrix_id,
            fields=fields,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            params: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete CRM status element.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/status/crm-status-delete.html

        This method deletes a directory element.

        Args:
            bitrix_id: Identifier of the directory element;

            params: Set of parameters, where FORCED is a flag for forcibly deleting system elements;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        _params = {
            "id": bitrix_id,
        }

        if params is not None:
            _params["params"] = params

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=_params,
            timeout=timeout,
        )
