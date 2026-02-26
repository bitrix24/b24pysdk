from typing import Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Event",
]


class Event(BaseEntity):
    """Handle operations related to Bitrix24 business process events.

    Documentation: https://apidocs.bitrix24.com/api-reference/bizproc/bizproc-robot/index.html
    """

    @type_checker
    def send(
            self,
            event_token: Text,
            return_values: JSONDict,
            *,
            log_message: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Return parameters to the action or Automation rule.

        Documentation: https://apidocs.bitrix24.com/api-reference/bizproc/bizproc-robot/bizproc-event-send.html

        This method sends an event to a Bitrix24 business process using the specified event token
        and return values, allowing the process to complete or trigger the next action with the
        returned parameters.

        Args:
            event_token: Unique token representing the process event;

            return_values: Object format:
                {
                    "PARAMETER_1": "value_1",

                    "PARAMETER_2": "value_2",

                    ...,

                    "PARAMETER_N": "value_N",
                };

            log_message: Optional log message to associate with the event;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "EVENT_TOKEN": event_token,
            "RETURN_VALUES": return_values,
        }

        if log_message is not None:
            params["LOG_MESSAGE"] = log_message

        return self._make_bitrix_api_request(
            api_wrapper=self.send,
            params=params,
            timeout=timeout,
        )
