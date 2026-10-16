from functools import cached_property
from typing import Annotated, Literal, Optional, Text, Union

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.converters import bool_to_bitrix
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity
from .history import History
from .personal import Personal
from .read import Read
from .schema import Schema
from .system import System

__all__ = [
    "Notify",
]


class Notify(BaseEntity):
    """Class for managing chat notifications.

    Documentation: https://apidocs.bitrix24.com/api-reference/chats/notifications/index.html
    """

    @cached_property
    def personal(self) -> Personal:
        """"""
        return Personal(self)

    @cached_property
    def history(self) -> History:
        """"""
        return History(self)

    @cached_property
    def read(self) -> Read:
        """"""
        return Read(self)

    @cached_property
    def schema(self) -> Schema:
        """"""
        return Schema(self)

    @cached_property
    def system(self) -> System:
        """"""
        return System(self)

    @type_checker
    def __call__(
            self,
            user_id: int,
            message: Text,
            *,
            type: Optional[Annotated[Text, Literal["USER", "SYSTEM"]]] = MISSING,
            message_out: Optional[Text] = MISSING,
            tag: Optional[Text] = MISSING,
            sub_tag: Optional[Text] = MISSING,
            attach: Optional[Union[JSONDict, Text]] = MISSING,
            client_id: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[Union[int, bool]]:
        """Send notification

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/notifications/im-notify.html

        The method sends a notification to a user.

        Args:
            user_id: User identifier;

            message: The text of notification;

            type: The type of notification;

            message_out: The text of notification for external channels;

            tag: A unique tag for the notification within the application;

            sub_tag: An additional notification tag without uniqueness checks;

            attach: An attachment for the notification in object format or JSON string;

            client_id: The application identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "USER_ID": user_id,
            "MESSAGE": message,
        }

        if type is not MISSING:
            params["TYPE"] = type

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
            api_wrapper=self,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def answer(
            self,
            notify_id: int,
            answer_text: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """Responding to notifications with quick response

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/notifications/im-notify-answer.html

        The method sends a text quick response to a notification.

        Args:
            notify_id: The identifier of the notification that supports a quick response;

            answer_text: The text of the quick response;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "NOTIFY_ID": notify_id,
            "ANSWER_TEXT": answer_text,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.answer,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def confirm(
            self,
            notify_id: int,
            notify_value: bool,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """Interacting with notification buttons

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/notifications/im-notify-confirm.html

        The method sends the selected value of the notification button.

        Args:
            notify_id: The identifier of the notification that supports a quick response;

            notify_value: Value of the selected button;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "NOTIFY_ID": notify_id,
            "NOTIFY_VALUE": bool_to_bitrix(notify_value, is_required=True),
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.confirm,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            *,
            bitrix_id: Optional[int] = MISSING,
            tag: Optional[Text] = MISSING,
            sub_tag: Optional[Text] = MISSING,
            client_id: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Delete notification

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/notifications/im-notify-delete.html

        The method removes a notification by ID or by tags.

        Args:
            bitrix_id: Identifier of the notification to be deleted;

            tag: Unique tag of the notification within the application;

            sub_tag: Additional tag of the notification;

            client_id: This parameter is required only for webhooks;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if bitrix_id is not MISSING:
            params["ID"] = bitrix_id

        if tag is not MISSING:
            params["TAG"] = tag

        if sub_tag is not MISSING:
            params["SUB_TAG"] = sub_tag

        if client_id is not MISSING:
            params["CLIENT_ID"] = client_id

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            *,
            last_id: Optional[int] = MISSING,
            last_type: Optional[Literal[1, 3]] = MISSING,
            limit: Optional[int] = MISSING,
            convert_text: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """Get notifications

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/notifications/im-notify-get.html

        The method returns a list of users notifications in parts.

        Args:
            last_id: Identifier of the last notification from the previous page to load the next one;

            last_type: Technical pagination cursor;

            limit: Number of notifications per page;

            convert_text: Convert notification text;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if last_id is not MISSING:
            params["LAST_ID"] = last_id

        if last_type is not MISSING:
            params["LAST_TYPE"] = last_type

        if limit is not MISSING:
            params["LIMIT"] = limit

        if convert_text is not MISSING:
            params["CONVERT_TEXT"] = bool_to_bitrix(convert_text, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params or None,
            timeout=timeout,
        )
