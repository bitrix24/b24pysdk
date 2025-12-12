from typing import Optional, Text

from ..bitrix_api.requests import BitrixAPIRequest
from ..utils.functional import type_checker
from ..utils.types import JSONDict, Timeout
from ._base_scope import BaseScope

__all__ = [
    "Placement",
]


class Placement(BaseScope):
    """Handle operations related to Bitrix24 widget placements.

    Documentation: https://apidocs.bitrix24.com/api-reference/widgets/index.html
    """

    @type_checker
    def bind(
            self,
            placement: Text,
            handler: Text,
            *,
            title: Optional[Text] = None,
            description: Optional[Text] = None,
            group_name: Optional[Text] = None,
            lang_all: Optional[JSONDict] = None,
            options: Optional[JSONDict] = None,
            user_id: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Register a widget placement handler.

        Documentation: https://apidocs.bitrix24.com/api-reference/widgets/placement-bind.html

        This method adds a handler for embedding a widget. It can be called at any time during the application operation but is mostly used during app installation.

        Args:
            placement: ID of the widget placement location;
            handler: URL of the widget placement handler;
            title: Widget's title in the interface;
            description: Description of the widget in the interface;
            group_name: Groups UI elements for multiple handlers of the same widget type;
            lang_all: Array of TITLE, DESCRIPTION, and GROUP_NAME parameters for specified languages;
            options: Additional widget display parameters;
            user_id: ID of the Bitrix24 user for whom the registered widget will be available;
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "PLACEMENT": placement,
            "HANDLER": handler,
        }

        if title is not None:
            params["TITLE"] = title

        if description is not None:
            params["DESCRIPTION"] = description

        if group_name is not None:
            params["GROUP_NAME"] = group_name

        if lang_all is not None:
            params["LANG_ALL"] = lang_all

        if options is not None:
            params["OPTIONS"] = options

        if user_id is not None:
            params["USER_ID"] = user_id

        return self._make_bitrix_api_request(
            api_wrapper=self.bind,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve registered widget placement handlers.

        Documentation: https://apidocs.bitrix24.com/api-reference/widgets/placement-get.html

        Fetches a list of registered handlers for widget placements.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            scope: Optional[Text] = None,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Get available widget placements.

        Documentation: https://apidocs.bitrix24.com/api-reference/widgets/placement-list.html

        Returns a list of available widget placement locations for the app.

        Args:
            scope: Restrict the list to a specific app access scope;
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = dict()

        if scope is not None:
            params["SCOPE"] = scope

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unbind(
            self,
            placement: Text,
            handler: Optional[Text] = None,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Remove a widget placement handler.

        Documentation: https://apidocs.bitrix24.com/api-reference/widgets/placement-unbind.html

        This method removes a registered handler for a widget placement and returns the count of removed handlers.

        Args:
            placement: ID of the widget placement location;
            handler: URL of the widget placement handler. If not specified, all handlers of the given location registered by the app will be removed;
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "PLACEMENT": placement,
        }

        if handler is not None:
            params["HANDLER"] = handler

        return self._make_bitrix_api_request(
            api_wrapper=self.unbind,
            params=params,
            timeout=timeout,
        )
