from functools import cached_property

from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity
from .status import Status

__all__ = [
    "Job",
]


class Job(BaseEntity):
    """Class for working with job synchronization.

    Documentation: https://apidocs.bitrix24.com/api-reference/sign/hcm-link/index.html
    """

    @cached_property
    def status(self) -> Status:
        """"""
        return Status(self)

    @type_checker
    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Update HCM link job

        Documentation: https://apidocs.bitrix24.com/api-reference/sign/hcm-link/humanresources-hcmlink-job-update.html

        The method updates an HCM link synchronization job.

        Args:
            bitrix_id: Synchronization job ID;

            fields: Job data;

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
