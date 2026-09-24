from typing import List, Text

from .._constants import MISSING
from ..api.requests import BitrixAPIRequest, BitrixAPIValueRequest, BitrixAPIValuesRequest
from ..objects.placement import Placement as PlacementObject
from ..schemas.results import CountResultData
from ..utils.functional import type_checker
from ..utils.types import JSONDict, JSONList, Timeout
from ._adapters import BitrixObjectsAdapter, BitrixResultAdapter
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
            title: Text = MISSING,
            description: Text = MISSING,
            group_name: Text = MISSING,
            lang_all: JSONDict = MISSING,
            options: JSONDict = MISSING,
            user_id: int = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Register a widget placement handler.

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
            Lazy request containing the registration success flag.
        """

        params: JSONDict = {
            "PLACEMENT": placement,
            "HANDLER": handler,
        }

        if title is not MISSING:
            params["TITLE"] = title

        if description is not MISSING:
            params["DESCRIPTION"] = description

        if group_name is not MISSING:
            params["GROUP_NAME"] = group_name

        if lang_all is not MISSING:
            params["LANG_ALL"] = lang_all

        if options is not MISSING:
            params["OPTIONS"] = options

        if user_id is not MISSING:
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
    ) -> BitrixAPIValuesRequest[JSONList, PlacementObject]:
        """Retrieve registered widget placement handlers as SDK objects.

        Documentation: https://apidocs.bitrix24.com/api-reference/widgets/placement-get.html

        Fetches a list of registered handlers for widget placements.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Lazy values request containing ``PlacementObject`` instances.
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValuesRequest,
            result_adapter=BitrixObjectsAdapter("placement", client=self._client),
        )

    @type_checker
    def list(
            self,
            *,
            scope: Text = MISSING,
            full: bool = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[List[Text]]:
        """
        Get available widget placements.

        Documentation: https://apidocs.bitrix24.com/api-reference/widgets/placement-list.html

        Returns a list of available widget placement locations for the app.

        Args:
            scope: Restrict the list to a specific app access scope;
            full: Whether to return all available placement locations regardless of the app access scopes;
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {}

        if scope is not MISSING:
            params["SCOPE"] = scope

        if full is not MISSING:
            params["FULL"] = full

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unbind(
            self,
            placement: Text,
            *,
            handler: Text = MISSING,
            user_id: int = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIValueRequest[CountResultData, int]:
        """
        Remove a widget placement handler.

        Documentation: https://apidocs.bitrix24.com/api-reference/widgets/placement-unbind.html

        This method removes a registered handler for a widget placement and returns the count of removed handlers.

        Args:
            placement: ID of the widget placement location;
            handler: URL of the widget placement handler. If not specified, all handlers of the given location registered by the app will be removed;
            user_id: ID of the Bitrix24 user for whom the handler was registered. If specified, only handlers registered for this user will be removed;
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIValueRequest.
        """

        params: JSONDict = {
            "PLACEMENT": placement,
        }

        if handler is not MISSING:
            params["HANDLER"] = handler

        if user_id is not MISSING:
            params["USER_ID"] = user_id

        return self._make_bitrix_api_request(
            api_wrapper=self.unbind,
            params=params,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValueRequest,
            result_adapter=BitrixResultAdapter(int, wrapper="count"),
        )
