from typing import Iterable, Optional

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.converters import bool_to_bitrix
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Read",
]


class Read(BaseEntity):
    """Class for managing 'read' status of notifications.

    Documentation: https://apidocs.bitrix24.com/api-reference/chats/notifications/index.html
    """

    @type_checker
    def __call__(
            self,
            bitrix_id: int,
            *,
            action: Optional[bool] = MISSING,
            only_current: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Read or mark notification as unread

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/notifications/im-notify-read.html

        The method marks a notification or all notifications as read or unread based on the specified parameters.

        Args:
            bitrix_id: Notification identifier;

            action: Action on the notification;

            only_current: The value Y changes only the notification with the specified ID;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "ID": bitrix_id,
        }

        if action is not MISSING:
            params["ACTION"] = bool_to_bitrix(action, is_required=True)

        if only_current is not MISSING:
            params["ONLY_CURRENT"] = bool_to_bitrix(only_current, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            ids: Iterable[int],
            *,
            action: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Read the list of notifications

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/notifications/im-notify-read-list.html

        The method marks a list of notifications as read or unread.

        Args:
            ids: An array of notification identifiers;

            action: Action on the notification;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if ids.__class__ is not list:
            ids = list(ids)

        params = {
            "IDS": ids,
        }

        if action is not MISSING:
            params["ACTION"] = bool_to_bitrix(action, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def all(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """Read all notification

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/notifications/im-notify-read-all.html

        The method marks all notifications of the current user as read.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.all,
            timeout=timeout,
        )
