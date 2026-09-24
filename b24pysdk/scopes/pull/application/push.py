from typing import Iterable, Text, Union

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Push",
]


class Push(BaseEntity):
    """Methods for real-time Push&Pull communication, including connection setup, event sending, and push notifications.

    Documentation: https://apidocs.bitrix24.com/settings/interactivity/push-and-pull/index.html
    """

    @type_checker
    def add(
            self,
            user_id: Union[int, Iterable[int]],
            text: Text,
            *,
            avatar: Text = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Send push notification to mobile device

        Documentation: https://apidocs.bitrix24.com/settings/interactivity/push-and-pull/pull-application-push-add.html

        The method sends a push notification to a mobile device within the application.

        Args:
            user_id: The user identifier or an array of user identifiers;

            text: Text of the push notification;

            avatar: URL of the image for the push notification;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if user_id.__class__ is not list and not isinstance(user_id, int):
            user_id = list(user_id)

        params = {
            "USER_ID": user_id,
            "TEXT": text,
        }

        if avatar is not MISSING:
            params["AVATAR"] = avatar

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )
