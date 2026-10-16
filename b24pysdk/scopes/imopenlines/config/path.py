from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Path",
]


class Path(BaseEntity):
    """Class for retrieving links to the public page of open channels.

    Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/index.html
    """

    @type_checker
    def get(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get link to public of open channels

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/imopenlines-config-path-get.html

        The method retrieves the link to the public page of open channels on the account.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            timeout=timeout,
        )
