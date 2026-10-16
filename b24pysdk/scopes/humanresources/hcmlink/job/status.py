from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "Status",
]


class Status(BaseEntity):
    """Class for checking activity of job synchronization.

    Documentation: https://apidocs.bitrix24.com/api-reference/sign/hcm-link/index.html
    """

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """Get HCM link job Status

        Documentation: https://apidocs.bitrix24.com/api-reference/sign/hcm-link/humanresources-hcmlink-job-status-get.html

        The method checks whether an HCM link synchronization job is active.

        Args:
            bitrix_id: Synchronization job ID;

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
