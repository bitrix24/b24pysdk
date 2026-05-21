from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import Timeout
from .._base_entity import BaseEntity

__all__ = [
    "AttachedObject",
]


class AttachedObject(BaseEntity):
    """The method helps handle attached file links.

    Documentation: https://apidocs.bitrix24.com/api-reference/disk/attached-object/index.html
    """

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get information about attached file

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/attached-object/disk-attached-object-get.html

        The method returns information about the attached file.

        Args:
            bitrix_id: Identifier of the file attachment record, which is the link connecting the disk file with other objects;

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

