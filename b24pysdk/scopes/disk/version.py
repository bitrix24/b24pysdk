from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Version",
]


class Version(BaseEntity):
    """The method helps handle file versions.

    Documentation: https://apidocs.bitrix24.com/api-reference/disk/version/index.html
    """

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get file version

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/version/disk-version-get.html

        The method returns the version of a file.

        Args:
            bitrix_id: Identifier of the file version;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

