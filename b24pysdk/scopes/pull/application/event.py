from typing import Iterable, Optional, Text, Union

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Event",
]


class Event(BaseEntity):
    """Methods for real-time Push&Pull communication, including connection setup, event sending, and push notifications.

    Documentation: https://apidocs.bitrix24.com/settings/interactivity/push-and-pull/index.html
    """

    @type_checker
    def add(
            self,
            command: Text,
            *,
            params: Optional[JSONDict] = MISSING,
            module_id: Optional[Text] = MISSING,
            user_id: Optional[Union[int, Iterable[int]]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Send events to the RT channel

        Documentation: https://apidocs.bitrix24.com/settings/interactivity/push-and-pull/pull-application-event-add.html

        The method sends an event to the RT channel of the application.

        Args:
            command: The event command;

            params: Event parameters;

            module_id: The identifier of the event module;

            user_id: The user identifier or an array of user identifiers;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        api_params = {
            "COMMAND": command,
        }

        if params is not MISSING:
            if params.__class__ is not list:
                params = list(params)

            api_params["PARAMS"] = params

        if module_id is not MISSING:
            api_params["MODULE_ID"] = module_id

        if user_id is not MISSING:
            if user_id.__class__ is not list and not isinstance(user_id, int):
                user_id = list(user_id)

            api_params["USER_ID"] = user_id

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=api_params,
            timeout=timeout,
        )
