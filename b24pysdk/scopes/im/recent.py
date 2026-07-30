from typing import Optional, Text, Union

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import B24BoolStrict, JSONDict, JSONList, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Recent",
]


class Recent(BaseEntity):
    """Special Operations in Chats

    Documentation: https://apidocs.bitrix24.com/api-reference/chats/special-operations/index.html
    """

    @type_checker
    def get(
            self,
            *,
            skip_openlines: Optional[Union[bool, B24BoolStrict]] = MISSING,
            skip_chat: Optional[Union[bool, B24BoolStrict]] = MISSING,
            skip_dialog: Optional[Union[bool, B24BoolStrict]] = MISSING,
            last_update: Optional[Text] = MISSING,
            only_openlines: Optional[Union[bool, B24BoolStrict]] = MISSING,
            last_sync_date: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONList]:
        """Get a shortened list of recent chats

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/im-recent-get.html

        The method retrieves a list of the user's recent chats.

        Args:
            skip_openlines: Skip chats from Open Channels;

            skip_chat: Skip group chats;

            skip_dialog: Skip one-on-one dialogs;

            last_update: Retrieve data from the specified date in ATOM (ISO-8601) format;

            only_openlines: Select only chats from Open Channels;

            last_sync_date: Date of the previous retrieval in ATOM (ISO-8601) format;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if skip_openlines is not MISSING:
            params["SKIP_OPENLINES"] = B24BoolStrict(skip_openlines).to_b24()

        if skip_chat is not MISSING:
            params["SKIP_CHAT"] = B24BoolStrict(skip_chat).to_b24()

        if skip_dialog is not MISSING:
            params["SKIP_DIALOG"] = B24BoolStrict(skip_dialog).to_b24()

        if last_update is not MISSING:
            params["LAST_UPDATE"] = last_update

        if only_openlines is not MISSING:
            params["ONLY_OPENLINES"] = B24BoolStrict(only_openlines).to_b24()

        if last_sync_date is not MISSING:
            params["LAST_SYNC_DATE"] = last_sync_date

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def list(  # noqa: C901, PLR0912
            self,
            *,
            skip_openlines: Optional[Union[bool, B24BoolStrict]] = MISSING,
            skip_dialog: Optional[Union[bool, B24BoolStrict]] = MISSING,
            skip_chat: Optional[Union[bool, B24BoolStrict]] = MISSING,
            last_message_date: Optional[Text] = MISSING,
            unread_only: Optional[Union[bool, B24BoolStrict]] = MISSING,
            parse_text: Optional[Union[bool, B24BoolStrict]] = MISSING,
            get_original_text: Optional[Union[bool, B24BoolStrict]] = MISSING,
            skip_undistributed_openlines: Optional[Union[bool, B24BoolStrict]] = MISSING,
            only_copilot: Optional[Union[bool, B24BoolStrict]] = MISSING,
            only_channel: Optional[Union[bool, B24BoolStrict]] = MISSING,
            can_manage_messages: Optional[Union[bool, B24BoolStrict]] = MISSING,
            offset: Optional[int] = MISSING,
            limit: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """Get the list of chats

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/im-recent-list.html

        The method retrieves a list of the user's recent conversations with pagination support.

        Args:
            skip_openlines: Skip chats from Open Channels;

            skip_chat: Skip group chats;

            skip_dialog: Skip one-on-one dialogs;

            last_message_date: Date of the last item from the previous selection in ATOM (ISO-8601) format;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if skip_openlines is not MISSING:
            params["SKIP_OPENLINES"] = B24BoolStrict(skip_openlines).to_b24()

        if skip_dialog is not MISSING:
            params["SKIP_DIALOG"] = B24BoolStrict(skip_dialog).to_b24()

        if skip_chat is not MISSING:
            params["SKIP_CHAT"] = B24BoolStrict(skip_chat).to_b24()

        if last_message_date is not MISSING:
            params["LAST_MESSAGE_DATE"] = last_message_date

        if unread_only is not MISSING:
            params["UNREAD_ONLY"] = B24BoolStrict(unread_only).to_b24()

        if parse_text is not MISSING:
            params["PARSE_TEXT"] = B24BoolStrict(parse_text).to_b24()

        if get_original_text is not MISSING:
            params["GET_ORIGINAL_TEXT"] = B24BoolStrict(get_original_text).to_b24()

        if skip_undistributed_openlines is not MISSING:
            params["SKIP_UNDISTRIBUTED_OPENLINES"] = B24BoolStrict(skip_undistributed_openlines).to_b24()

        if only_copilot is not MISSING:
            params["ONLY_COPILOT"] = B24BoolStrict(only_copilot).to_b24()

        if only_channel is not MISSING:
            params["ONLY_CHANNEL"] = B24BoolStrict(only_channel).to_b24()

        if can_manage_messages is not MISSING:
            params["CAN_MANAGE_MESSAGES"] = B24BoolStrict(can_manage_messages).to_b24()

        if offset is not MISSING:
            params["OFFSET"] = offset

        if limit is not MISSING:
            params["LIMIT"] = limit

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def hide(
            self,
            dialog_id: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Remove chat from the recent list

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/special-operations/im-recent-hide.html

        The method removes a dialog from the list of recent chats for the current user.

        Args:
            dialog_id: Identifier of the chat;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            DIALOG_ID=dialog_id,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.hide,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def pin(
            self,
            dialog_id: Text,
            pin: Union[bool, B24BoolStrict],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Pin a chat at the top

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/special-operations/im-recent-pin.html

        The method pins or unpins a conversation at the top of the user's chat list.

        Args:
            dialog_id: Identifier of the chat;

            pin: Pin or unpin the conversation;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            DIALOG_ID=dialog_id,
            PIN=B24BoolStrict(pin).to_b24(),
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.pin,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unread(
            self,
            dialog_id: Text,
            action: Union[bool, B24BoolStrict],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Set or remove thr "Read" flag for the chat

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/special-operations/im-recent-unread.html

        The method sets or removes the "read" flag for the chat.

        Args:
            dialog_id: Identifier of the chat;

            action: Action for the "read" flag;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            DIALOG_ID=dialog_id,
            ACTION=B24BoolStrict(action).to_b24(),
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.unread,
            params=params,
            timeout=timeout,
        )
