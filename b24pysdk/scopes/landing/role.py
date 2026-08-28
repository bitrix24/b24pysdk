from typing import Iterable, Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Role",
]


class Role(BaseEntity):
    """Class for managing role-based access model

    Documentation: https://apidocs.bitrix24.com/api-reference/landing/rights/role-model/index.html
    """

    @type_checker
    def enable(
            self,
            mode: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Enable or disable role-based access model

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/rights/landing-role-enable.html

        The method enables or disables the role-based access model for the "Sites and Stores" section.

        Args:
            mode: Access model mode;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "mode": mode,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.enable,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def is_enabled(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Check if the role model of permissions is enabled

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/rights/landing-role-is-enabled.html

        The method checks whether the role model of permissions is enabled for the "Sites and Stores" section.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.is_enabled,
            params=None,
            timeout=timeout,
        )

    @type_checker
    def get_list(
            self,
            *,
            scope: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of roles

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/rights/role-model/landing-role-get-list.html

        The method retrieves a list of access roles for the selected type of sites.

        Args:
            scope: The type of sites for which roles need to be retrieved;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if scope is not MISSING:
            params["scope"] = scope

        return self._make_bitrix_api_request(
            api_wrapper=self.get_list,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def get_rights(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get role rights

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/rights/role-model/landing-role-get-rights.html

        The method returns the rights of the specified role for each site where they are configured.

        Args:
            bitrix_id: Role identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get_rights,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set_rights(
            self,
            bitrix_id: int,
            rights: JSONDict,
            *,
            additional: Optional[Iterable[Text]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Set role permissions for the site list

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/rights/role-model/landing-role-set-rights.html

        The method sets role permissions for sites.

        Args:
            bitrix_id: The identifier of the role for which permissions need to be updated;

            rights: Object format:

                {
                    "0": ["read"],

                    "<siteId>": ["read", "edit", "sett"]
                }

                where:

                - 0 — default permission for sites without separate settings

                - <siteId> — site identifier;

            additional: Additional capabilities of the role;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if additional is not MISSING and additional.__class__ is not list:
            additional = list(additional)

        params: JSONDict = {
            "id": bitrix_id,
            "rights": rights,
        }

        if additional is not MISSING:
            params["additional"] = additional

        return self._make_bitrix_api_request(
            api_wrapper=self.set_rights,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set_access_codes(
            self,
            bitrix_id: int,
            *,
            codes: Optional[Iterable[Text]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Set access codes for roles

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/rights/role-model/landing-role-set-access-codes.html

        The method specifies to whom the role is assigned: users, groups, or departments.

        Args:
            bitrix_id: Role identifier;

            codes: The final list of access codes for the role;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        if codes is not MISSING:
            if codes.__class__ is not list:
                codes = list(codes)

            params["codes"] = codes

        return self._make_bitrix_api_request(
            api_wrapper=self.set_access_codes,
            params=params,
            timeout=timeout,
        )
