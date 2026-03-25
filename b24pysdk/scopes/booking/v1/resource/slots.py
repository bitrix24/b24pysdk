from typing import Iterable

from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "Slots",
]


class Slots(BaseEntity):
    """Handle operations related to Bitrix24 booking resource slots.

    Documentation: https://apidocs.bitrix24.com/api-reference/booking/resource/slots/index.html
    """

    @type_checker
    def list(
            self,
            resource_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve the time slot configuration for a specific resource.

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/resource/slots/booking-v1-resource-slots-list.html

        The method returns the configuration of time slots for the specified resource.

        Args:
            resource_id: Identifier of the resource;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "resourceId": resource_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set(
            self,
            resource_id: int,
            slots: Iterable[JSONDict],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Set time slots for a specific resource.

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/resource/slots/booking-v1-resource-slots-set.html

        The method allows you to set time slots for the specified resource.

        Args:
            resource_id: Identifier of the resource;

            slots: Object format:
                [
                    {
                        "from": integer,
                        "to": integer,
                        "timezone": "TZ database name",
                        "weekDays": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                        "slotSize": integer,
                    }
                ];

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        if slots.__class__ is not list:
            slots = list(slots)

        params = {
            "resourceId": resource_id,
            "slots": slots,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.set,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unset(
            self,
            resource_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Delete the time slot configuration for a specific resource.

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/resource/slots/booking-v1-resource-slots-unset.html

        The method removes the time slot settings for the specified resource.

        Args:

            resource_id: Identifier of the resource;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "resourceID": resource_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.unset,
            params=params,
            timeout=timeout,
        )
