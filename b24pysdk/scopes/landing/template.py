from typing import Optional

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Template",
]


class Template(BaseEntity):
    """Methods for working with a structure that Bitrix24 uses to assemble a website page.

    Documentation: https://apidocs.bitrix24.com/api-reference/landing/template/index.html"""

    @type_checker
    def getlist(
            self,
            *,
            params: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of view templates

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/template/landing-template-get-list.html

        The method retrieves a list of view templates for the current account based on the selection parameters.

        Args:
            params: An object containing the selection parameters for view templates;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        _params: JSONDict = {}

        if params is not MISSING:
            _params["params"] = params
        return self._make_bitrix_api_request(
            api_wrapper=self.getlist,
            params=_params or None,
            timeout=timeout,
        )

    @type_checker
    def get_landing_ref(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of included areas for the page

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/template/landing-template-get-landing-ref.html

        The method retrieves a list of included areas associated with the page.

        Args:
            bitrix_id: The identifier of the page;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get_landing_ref,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_site_ref(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of included areas for the site

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/template/landing-template-get-site-ref.html

        The method retrieves a list of included areas associated with the site.

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
            api_wrapper=self.get_site_ref,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set_landing_ref(
            self,
            bitrix_id: int,
            *,
            data: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Set included areas for page

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/template/landing-template-set-landing-ref.html

        The method sets the bindings of included areas for the page.

        Args:
            bitrix_id: Identifier of the page;

            data: Set of bindings for the included areas of the page;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        if data is not MISSING:
            params["data"] = data

        return self._make_bitrix_api_request(
            api_wrapper=self.set_landing_ref,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set_site_ref(
            self,
            bitrix_id: int,
            *,
            data: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Set included areas for the site

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/template/landing-template-set-site-ref.html

        The method saves the bindings of included areas for the site.

        Args:
            bitrix_id: Identifier of the site;

            data: A set of bindings for the included areas of the site;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        if data is not MISSING:
            params["data"] = data

        return self._make_bitrix_api_request(
            api_wrapper=self.set_site_ref,
            params=params,
            timeout=timeout,
        )
