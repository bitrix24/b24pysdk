from typing import Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.converters import bool_to_bitrix
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "SysPage",
]


class SysPage(BaseEntity):
    """Methods for managing special type website pages.

    Documentation: https://apidocs.bitrix24.com/api-reference/landing/page/special-pages/index.html
    """

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            active: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of special pages

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/page/special-pages/landing-syspage-get.html

        The method returns a list of special pages for the site.

        Args:
            bitrix_id: Identifier of the site;

            active: Return only pages that are not deleted and are active;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        if active is not MISSING:
            params["active"] = bool_to_bitrix(active, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def get_special_page(
            self,
            site_id: int,
            type: Text,
            *,
            additional: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the URL of the special page

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/page/special-pages/landing-syspage-get-special-page.html

        The method returns the URL of the special page for the site.

        Args:
            site_id: Site identifier;

            type: The code of the special page that the method looks for in the site's bindings;

            additional: Additional URL parameters;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "siteId": site_id,
            "type": type,
        }

        if additional is not MISSING:
            params["additional"] = additional

        return self._make_bitrix_api_request(
            api_wrapper=self.get_special_page,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set(
            self,
            bitrix_id: int,
            type: Text,
            *,
            lid: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Set a special page for the site

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/page/special-pages/landing-syspage-set.html

        The method assigns a special page for the site.

        Args:
            bitrix_id: Identifier of the site;

            type: The code of the special page;

            lid: Identifier of the page to be set as special for the site;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
            "type": type,
        }

        if lid is not MISSING:
            params["lid"] = lid

        return self._make_bitrix_api_request(
            api_wrapper=self.set,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete_for_site(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete all bindings of special pages for site

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/page/special-pages/landing-syspage-delete-for-site.html

        The method removes all bindings of special pages for the site.

        Args:
            bitrix_id: Identifier of the site;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete_for_site,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete_for_landing(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete all page bindings as special

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/page/special-pages/landing-syspage-delete-for-landing.html

        The method removes all bindings where the page with the identifier id is designated as special for the site.

        Args:
            bitrix_id: Identifier of the site;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete_for_landing,
            params=params,
            timeout=timeout,
        )
