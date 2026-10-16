from typing import Optional, Text, Union

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Personal",
]


class Personal(BaseEntity):
    """Class for sending personal notifications.

    Documentation: https://apidocs.bitrix24.com/api-reference/chats/notifications/index.html
    """

    @type_checker
    def add(
            self,
            user_id: int,
            message: Text,
            *,
            message_out: Optional[Text] = MISSING,
            tag: Optional[Text] = MISSING,
            sub_tag: Optional[Text] = MISSING,
            attach: Optional[Union[JSONDict, Text]] = MISSING,
            client_id: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[Union[int, bool]]:
        """Send personal notification

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/notifications/im-notify-personal-add.html

        The method sends a personal notification on behalf of the current user.

        Args:
            user_id: User identifier;

            message: The text of the notification;

            message_out: The text of the notification for the external channels;

            tag: A unique tag for the notification within the application;

            sub_tag: An additional tag for the notification without uniqueness checks;

            attach: Attachment for the notification in object format or JSON string;

            client_id: The application identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "USER_ID": user_id,
            "MESSAGE": message,
        }

        if message_out is not MISSING:
            params["MESSAGE_OUT"] = message_out

        if tag is not MISSING:
            params["TAG"] = tag

        if sub_tag is not MISSING:
            params["SUB_TAG"] = sub_tag

        if attach is not MISSING:
            params["ATTACH"] = attach

        if client_id is not MISSING:
            params["CLIENT_ID"] = client_id

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )
