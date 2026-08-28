from typing import Text

from ...api.requests import BitrixAPIRequest
from ...utils.converters import bool_to_bitrix
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "RepoWidget",
]


class RepoWidget(BaseEntity):
    """Class helps managing widgets on start page.

    Documentation: https://apidocs.bitrix24.com/api-reference/vibe/index.html
    """

    @type_checker
    def register(
            self,
            code: Text,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add widget to start page

        Documentation: https://apidocs.bitrix24.com/api-reference/vibe/landing-repowidget-register.html

        The method adds a widget for the Start page: the Vibe.

        Args:
            code: Unique code for the widget;

            fields: Field values for creating the widget;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "code": code,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.register,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unregister(
            self,
            code: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Unregister widget for Vibe

        Documentation: https://apidocs.bitrix24.com/api-reference/vibe/landing-repowidget-unregister.html

        The method removes the widget for Start page: the Vibe.

        Args:
            code: Unique code for the widget;

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

    @type_checker
    def getlist(
            self,
            params: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of widgets

        Documentation: https://apidocs.bitrix24.com/api-reference/vibe/landing-repowidget-get-list.html

        The method returns a list of widgets for the current application, filtered by the specified criteria.

        Args:
            params: Array of fields to retrieve the list of widgets;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        api_params: JSONDict = {
            "params": params,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.getlist,
            params=api_params,
            timeout=timeout,
        )

    @type_checker
    def debug(
            self,
            enable: bool,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Enable debug mode

        Documentation: https://apidocs.bitrix24.com/api-reference/vibe/landing-repowidget-debug.html

        The method enables debug mode for all widgets of the current application

        Args:
            enable: Debug mode activation flag;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "enable": bool_to_bitrix(enable, is_required=True),
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.debug,
            params=params,
            timeout=timeout,
        )
