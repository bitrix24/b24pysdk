from typing import Iterable, Text

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "Value",
]


class Value(BaseEntity):
    """Class for transferring values from HR system.

    Documentation: https://apidocs.bitrix24.com/api-reference/sign/hcm-link/index.html
    """

    @type_checker
    def set(
            self,
            company: Text,
            data: Iterable[JSONDict],
            *,
            job: JSONDict = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """Transfer HCM link fields values

        Documentation: https://apidocs.bitrix24.com/api-reference/sign/hcm-link/humanresources-hcmlink-field-value-set.html

        The method transfers HR system field values for employees.

        Args:
            company: Company code in the HR system or CRM company ID;

            data: List of fields values;

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
