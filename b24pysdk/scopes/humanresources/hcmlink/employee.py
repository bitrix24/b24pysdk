from typing import Iterable, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, JSONList, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Employee",
]


class Employee(BaseEntity):
    """Class for retrieving employees from HR systems and Bitrix24.

    Documentation: https://apidocs.bitrix24.com/api-reference/sign/hcm-link/index.html
    """

    @type_checker
    def list(
            self,
            company: Text,
            *,
            limit: int = MISSING,
            offset: int = MISSING,
            updated_at: Text = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONList]:
        """Get mapped HCM link employee list

        Documentation: https://apidocs.bitrix24.com/api-reference/sign/hcm-link/humanresources-hcmlink-employee-list.html

        The method retrieves a list of mapped employees from the HR system and Bitrix24.

        Args:
            company: Company code in the HR system;

            limit: Number of records per page;

            offset: Offset for page navigation;

            updated_at: Modification date in ISO 8601 format;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "company": company,
        }

        if limit is not MISSING:
            params["limit"] = limit

        if offset is not MISSING:
            params["offset"] = offset

        if updated_at is not MISSING:
            params["updatedAt"] = updated_at

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set(
            self,
            company: Text,
            data: Iterable[JSONDict],
            *,
            job: JSONDict = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """Transfer HCM link employee list

        Documentation: https://apidocs.bitrix24.com/api-reference/sign/hcm-link/humanresources-hcmlink-employee-set.html

        The method transfers a list of employees from an HR systemto the HCM link integration.

        Args:
            company: Company code in the HR system;

            data: List of employees from the HR system;

            job: Data for updating the synchronization job;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if data.__class__ is not list:
            data = list(data)

        params: JSONDict = {
            "company": company,
            "data": data,
        }

        if job is not MISSING:
            params["job"] = job

        return self._make_bitrix_api_request(
            api_wrapper=self.set,
            params=params,
            timeout=timeout,
        )
