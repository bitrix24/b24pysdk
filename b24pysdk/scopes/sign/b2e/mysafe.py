from typing import Optional

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Mysafe",
]


class Mysafe(BaseEntity):
    """Class for retrieving signed documents in the company's safe.

    Documentation: https://apidocs.bitrix24.com/api-reference/sign/index.html
    """

    @type_checker
    def tail(
            self,
            *,
            limit: Optional[int] = MISSING,
            offset: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of signed documents in the company's safe

        Documentation: https://apidocs.bitrix24.com/api-reference/sign/sign-b2e-mysafe-tail.html

        The method returns a list of signed documents in the company's safe.

        Args:
            limit: Number of records per page;

            offset: This parameter is used to manage pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if limit is not MISSING:
            params["limit"] = limit

        if offset is not MISSING:
            params["offset"] = offset

        return self._make_bitrix_api_request(
            api_wrapper=self.tail,
            params=params or None,
            timeout=timeout,
        )
