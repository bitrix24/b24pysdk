from functools import cached_property
from typing import Text

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity
from .booking import Booking

__all__ = [
    "Resource",
]


class Resource(BaseEntity):
    """Class for managing service provision for a specific time.

    Documentation: https://apidocs.bitrix24.com/api-reference/calendar/resource/index.html
    """

    @cached_property
    def booking(self) -> Booking:
        """"""
        return Booking(self)

    @type_checker
    def add(
            self,
            name: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add a new resource

        Documentation: https://apidocs.bitrix24.com/api-reference/calendar/resource/calendar-resource-add.html

        The method adds a new resource.

        Args:
            name: Resource name;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "name": name,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            resource_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete resource

        Documentation: https://apidocs.bitrix24.com/api-reference/calendar/resource/calendar-resource-delete.html

        The method deletes a resource.

        Args:
            resource_id: Resource ID;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "resourceId": resource_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of all resources

        Documentation: https://apidocs.bitrix24.com/api-reference/calendar/resource/calendar-resource-list.html

        The method retrieves a list of all resources.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            resource_id: int,
            name: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update resource

        Documentation: https://apidocs.bitrix24.com/api-reference/calendar/resource/calendar-resource-update.html

        The method updates a resource.

        Args:
            resource_id: Resource ID;

            name: New name of the resource;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "resourceId": resource_id,
            "name": name,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
