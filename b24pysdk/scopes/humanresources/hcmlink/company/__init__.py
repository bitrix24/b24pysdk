from functools import cached_property

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, JSONList, Timeout
from ...._base_entity import BaseEntity
from .user import User

__all__ = [
    "Company",
]


class Company(BaseEntity):
    """Class for managing companies from HR systems.

    Documentation: https://apidocs.bitrix24.com/api-reference/sign/hcm-link/index.html
    """

    @cached_property
    def user(self) -> User:
        """"""
        return User(self)

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[int]:
        """Add HCM link company

        Documentation: https://apidocs.bitrix24.com/api-reference/sign/hcm-link/humanresources-hcmlink-company-add.html

        The method adds a company from an HR system to the HCM link integration.

        Args:
            fields: Company data from the HR system;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Delete HCM link company

        Documentation: https://apidocs.bitrix24.com/api-reference/sign/hcm-link/humanresources-hcmlink-company-delete.html

        The method deletes a company from the HCM link integration.

        Args:
            bitrix_id: HCM link company ID;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            limit: int = MISSING,
            offset: int = MISSING,
            user_id: int = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONList]:
        """Get HCM link company list

        Documentation: https://apidocs.bitrix24.com/api-reference/sign/hcm-link/humanresources-hcmlink-company-list.html

        The method retrieves a list of companies connected to the HCM link integration.

        Args:
            limit: Number of records per page;

            offset: Offset for page navigation;

            user_id: Bitrix24 user ID;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if limit is not MISSING:
            params["limit"] = limit

        if offset is not MISSING:
            params["offset"] = offset

        if user_id is not MISSING:
            params["userId"] = user_id

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Update HCM link company

        Documentation: https://apidocs.bitrix24.com/api-reference/sign/hcm-link/humanresources-hcmlink-company-update.html

        The method updates a company from an HR system and the list of its fields in the HCM link integration.

        Args:
            bitrix_id: HCM link company ID;

            fields: New company data from the HR system;

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
