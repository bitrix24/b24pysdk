from typing import Optional

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Item",
]


class Item(BaseEntity):
    """A set of methods for working with workflow elements.

    Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/item/index.html
    """

    @type_checker
    def add(
            self,
            type_id: int,
            *,
            fields: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add process element

        Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/item/rpa-item-add.html

        This method adds a new process element with the identifier typeId.

        Args:
            type_id: Identifier of the process;

            fields: Values of the custom fields of the element;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "typeId": type_id,
        }

        if fields is not MISSING:
            params["fields"] = fields

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            type_id: int,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete element

        Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/item/rpa-item-delete.html

        This method deletes an element.

        Args:
            type_id: Identifier of the process;

            bitrix_id: Identifier of the element;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "typeId": type_id,
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            type_id: int,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get information about the element

        Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/item/rpa-item-get.html

        This method retrieves information about the element with the identifier id of the process with the identifier typeId.

        Args:
            type_id: Identifier of the process;

            bitrix_id: Identifier of the element;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "typeId": type_id,
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_tasks(
            self,
            type_id: int,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get data on current tasks of the element

        Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/item/rpa-item-get-tasks.html

        This method retrieves data on the current tasks of the element with the identifier id for the process with the identifier typeId.

        Args:
            type_id: Identifier of the process;

            bitrix_id: Identifier of the element;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "typeId": type_id,
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get_tasks,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            type_id: int,
            *,
            order: Optional[JSONDict] = MISSING,
            filter: Optional[JSONDict] = MISSING,
            start: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Retrieve an array of process elements

        Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/item/rpa-item-list.html

        This method retrieves a list of process elements with the identifier typeId.

        Args:
            type_id: Identifier of the process;

            order: List for sorting, where the key is the field and the value is ASC or DESC;

            filter: List for filtering;

            start: Offset for pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "typeId": type_id,
        }

        if order is not MISSING:
            params["order"] = order

        if filter is not MISSING:
            params["filter"] = filter

        if start is not MISSING:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            type_id: int,
            bitrix_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update process element

        Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/item/rpa-item-update.html

        This method updates the element with the identifier id in the process with the identifier typeId.

        Args:
            type_id: Identifier of the process;

            bitrix_id: Identifier of the element;

            fields: Object containing values for custom fields of the element;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "typeId": type_id,
            "id": bitrix_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
