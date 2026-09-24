from functools import cached_property
from typing import Optional

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity
from .slots import Slots

__all__ = [
    "Resource",
]


class Resource(BaseEntity):
    """Class for managing objects that can be reserved.

    Documentation: https://apidocs.bitrix24.com/api-reference/booking/resource/index.html
    """

    @cached_property
    def slots(self) -> Slots:
        """"""
        return Slots(self)

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add a new resource

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/resource/booking-v1-resource-add.html

        The method adds a new resource.

        Args:
            fields: An object containing field values for creating a resource;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
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
        """Delete resource

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/resource/booking-v1-resource-delete.html

        The method removes a resource.

        Args:
            bitrix_id: Resource identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
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
        """Get resource

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/resource/booking-v1-resource-get.html

        The method returns information about a resource by its identifier.

        Args:
             bitrix_id: Resource identifier;

             timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
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
            filter: Optional[JSONDict] = MISSING,
            order: Optional[JSONDict] = MISSING,
            start: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of resources

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/resource/booking-v1-resource-list.html

        The method return a lisr of resources based on a filter.

        Args:
            filter: An object for filtering the list of resources;

            order: An object for sorting the list of the resources;

            start: A parameter for managing pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if filter is not MISSING:
            params["filter"] = filter

        if order is not MISSING:
            params["order"] = order

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
            bitrix_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update resource

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/resource/booking-v1-resource-update.html

        The method updates an existing resource.

        Args:
            bitrix_id: Resource identifier;

            fields: An object containing field values for updating a resource;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
