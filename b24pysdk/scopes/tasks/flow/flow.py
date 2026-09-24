from typing import Text

from ....api.requests import BitrixAPIRequest
from ....utils.functional import classproperty, type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Flow",
]


class Flow(BaseEntity):
    """Class for managing flows in groups.

    Documentation: https://apidocs.bitrix24.com/api-reference/tasks/flow/index.html
    """

    @classproperty
    def _name(cls) -> Text:
        return "Flow"

    @type_checker
    def activate(
            self,
            flow_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Activate/Deactivate the flow

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/flow/tasks-flow-flow-activate.html

        The method turns the flow on or off by its identifier.

        Args:
            flow_id: The identifier of the flow to be activated or deactivated;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "flowId": flow_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.activate,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def create(
            self,
            flow_data: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create a new flow

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/flow/tasks-flow-flow-create.html

        The method creates a flow.

        Args:
            flow_data: Field values for creating the flow;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "flowData": flow_data,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.create,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            flow_data: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete flow

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/flow/tasks-flow-flow-delete.html

        The method deletes a flow by its identifier.

        Args:
            flow_data: Object containing ID for deleting the flow;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "flowData": flow_data,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            flow_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get flow

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/flow/tasks-flow-flow-get.html

        The method returns flow data by its identifier.

        Args:
            flow_id: The identifier of the flow to be retrieved;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "flowId": flow_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def is_exists(
            self,
            flow_data: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Check the existence

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/flow/tasks-flow-flow-is-exists.html

        The method checks whether a flow with the specified name exists.

        Args:
            flow_data: Object containing data to check for flow existence;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "flowData": flow_data,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.is_exists,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def pin(
            self,
            flow_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Pin or unpin the flow

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/flow/tasks-flow-flow-pin.html

        The method pins or unpins a flow in the list of flows by its identifier.

        Args:
            flow_id: The identifier of the flow to be pinned or unpinned;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "flowId": flow_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.pin,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            flow_data: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update the flow

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/flow/tasks-flow-flow-update.html

        The method modifies the flow.

        Args:
            flow_data: Field values to modify the flow;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "flowData": flow_data,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
