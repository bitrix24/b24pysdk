from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Schedule",
]


class Schedule(BaseEntity):
    """Class for retrieving work schedule.

    Documentation: https://apidocs.bitrix24.com/api-reference/timeman/schedule/index.html
    """

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get work schedule

        Documentation: https://apidocs.bitrix24.com/api-reference/timeman/schedule/timeman-schedule-get.html

        The method retrieves the work schedule by its identifier.

        Args:
            bitrix_id: Identifier of the schedule;

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
