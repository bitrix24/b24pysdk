from typing import Iterable, Text

from .....api.requests import BitrixAPIRequest
from .....utils.functional import classproperty, type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "ExternalData",
]


class ExternalData(BaseEntity):
    """
    Handle operations related to external data bindings for waitlist records.

    Documentation: https://apidocs.bitrix24.com/api-reference/booking/waitlist/external-data/index.html
    """

    @classproperty
    def _name(cls) -> Text:
        return "externalData"

    @type_checker
    def list(
            self,
            wait_list_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve external data bindings for a waitlist record.

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/waitlist/external-data/booking-v1-waitlist-externaldata-list.html

        Returns the list of linked external entities associated with the specified waitlist record.

        Args:
            wait_list_id: Identifier of the waitlist record (waitListId);

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "waitListId": wait_list_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set(
            self,
            wait_list_id: int,
            external_data: Iterable[JSONDict],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Set external data bindings for a waitlist record.

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/waitlist/external-data/booking-v1-waitlist-externaldata-set.html

        Creates or replaces the set of external entities linked to the specified waitlist record.

        Args:
            wait_list_id: Identifier of the waitlist record (waitListId);

            external_data: Array of objects containing objects for binding;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        if external_data.__class__ is not list:
            external_data = list(external_data)

        params = {
            "waitListId": wait_list_id,
            "externalData": external_data,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.set,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unset(
            self,
            wait_list_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Remove all external data bindings for a waitlist record.

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/waitlist/external-data/booking-v1-waitlist-externaldata-unset.html

        Deletes all links to external entities for the specified waitlist record.

        Args:
            wait_list_id: Identifier of the waitlist record;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "waitListId": wait_list_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.unset,
            params=params,
            timeout=timeout,
        )
