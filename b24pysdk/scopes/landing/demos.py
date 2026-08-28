from typing import Annotated, Literal, Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Demos",
]


class Demos(BaseEntity):
    """Class helps to manage custom templates.

    Documentation: https://apidocs.bitrix24.com/api-reference/landing/demos/index.html
    """

    @type_checker
    def get_list(
            self,
            *,
            params: Optional[JSONDict] = MISSING,
            start: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of registered templates

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/demos/landing-demos-get-list.html

        The method retrieves a list of registered templates.

        Args:
            params: Object format:
                {
                    select: value_1,

                    filter: value_2,

                    order: value_3,

                    group: value_4,

                    limit: value_5,

                    offset: value_6
                },

                where value_n — value of the corresponding selection parameter;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        api_params: JSONDict = {}

        if params is not MISSING:
            api_params["params"] = params

        if start is not MISSING:
            api_params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.get_list,
            params=api_params or None,
            timeout=timeout,
        )

    @type_checker
    def get_site_list(
            self,
            type: Annotated[Text, Literal["page", "store", "knowledge", "group", "mainpage"]],
            *,
            filter: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of templates for creating websites

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/demos/landing-demos-get-site-list.html

        The method landing.demos.getSiteList retrieves a list of file demo templates for websites.

        Args:
            type: Template type;

            filter: Object format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n
                },

                where:

                - field_n — filter field,
                - value_n — filter value;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "type": type,
        }

        if filter is not MISSING:
            params["filter"] = filter

        return self._make_bitrix_api_request(
            api_wrapper=self.get_site_list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_page_list(
            self,
            type: Annotated[Text, Literal["page", "store", "knowledge", "group", "mainpage"]],
            *,
            filter: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of templates for creating pages

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/demos/landing-demos-get-page-list.html

        The method landing.demos.getSiteList retrieves a list of file demo templates for pages.

        Args:
            type: Template type;

            filter: Object format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n
                },

                where:

                - field_n — filter field,
                - value_n — filter value;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "type": type,
        }

        if filter is not MISSING:
            params["filter"] = filter

        return self._make_bitrix_api_request(
            api_wrapper=self.get_page_list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def register(
            self,
            data: JSONDict,
            *,
            params: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Register a template in the site creation wizard

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/demos/landing-demos-register.html

        The method registers a custom template in the site and page creation wizard.

        Args:
            data: Template data;

            params: Additional registration parameters;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        api_params: JSONDict = {
            "data": data,
        }

        if params is not MISSING:
            api_params["params"] = params

        return self._make_bitrix_api_request(
            api_wrapper=self.register,
            params=api_params,
            timeout=timeout,
        )

    @type_checker
    def unregister(
            self,
            code: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete registered template

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/demos/landing-demos-unregister.html

        The method deletes a registered template by its code.

        Args:
            code: External code of the template;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "code": code,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.unregister,
            params=params,
            timeout=timeout,
        )
