from typing import Iterable, Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Type",
]


class Type(BaseEntity):
    """Methods for working with processes.

    Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/type/index.html
    """

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create process

        Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/type/rpa-type-add.html

        This method creates a new process.

        Args:
            fields: A list of process fields;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete process

        Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/type/rpa-type-delete.html

        This method deletes a process.

        Args:
            bitrix_id: The ID of the process;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
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
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get process information by ID

        Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/type/rpa-type-get.html

        This method retrieves information about a process by its id.

        Args:
            bitrix_id: The ID of the process;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            select: Optional[Iterable[Text]] = MISSING,
            order: Optional[JSONDict] = MISSING,
            filter: Optional[JSONDict] = MISSING,
            start: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Retrieve a list of process with their fields

        Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/type/rpa-type-list.html

        The method will return an array of processes with their fields.

        Args:
            select: Array of fields to output;

            order: List for sorting, where the key is the field and the value is ASC or DESC;

            filter: List for filtering;

            start: This parameter is used to manage pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        if order is not MISSING:
            params["order"] = order

        if filter is not MISSING:
            params["filter"] = filter

        if start is not MISSING:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params or None,
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
        """Update the process

        Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/type/rpa-type-update.html

        This method updates the process by its id.

        Args:
            bitrix_id: Identifier of the process;

            fields: List of process fields;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
