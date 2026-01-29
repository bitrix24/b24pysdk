from ...bitrix_api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Rights",
]


class Rights(BaseEntity):
    """
    Handle operations related to Bitrix24 Disk rights.

    Documentation: https://apidocs.bitrix24.com/api-reference/disk/rights/index.html
    """

    @type_checker
    def get_tasks(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve the list of access levels (tasks) available for assigning Disk rights.

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/rights/disk-rights-get-tasks.html

        This method calls disk.rights.getTasks to obtain access level definitions that can be used when assigning permissions.

        Args:
            timeout: Timeout in seconds;

        Returns:
            Instance of BitrixAPIRequest.
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.get_tasks,
            timeout=timeout,
        )


