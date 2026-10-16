from typing import Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.converters import bool_to_bitrix
from ....utils.functional import type_checker
from ....utils.types import JSONDict, JSONList, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Last",
]


class Last(BaseEntity):
    """Class for managing user's history search queries.

    Documentation: https://apidocs.bitrix24.com/api-reference/chats/search/index.html
    """

    @type_checker
    def add(
            self,
            dialog_id: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Add entry to search history

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/search/im-search-last-add.html

        The method adds a dialog to the last search history.

        Args:
            dialog_id: Identifier for the message object: user or chat;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            DIALOG_ID=dialog_id,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            dialog_id: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Delete record from search history

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/search/im-search-last-delete.html

        The method removes a dialog from the last search history.

        Args:
            dialog_id: Identifier for the message object: user or chat;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            DIALOG_ID=dialog_id,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            *,
            skip_openlines: Optional[bool] = MISSING,
            skip_chat: Optional[bool] = MISSING,
            skip_dialog: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONList]:
        """Get search history

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/search/im-search-last-get.html

        The method returns a list of dialogs from the history of the last search.

        Args:
            skip_openlines: Skip Open Channels chats;

            skip_chat: Skip group chat;

            skip_dialog: Skip personal dialogs;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if skip_openlines is not MISSING:
            params["SKIP_OPENLINES"] = bool_to_bitrix(skip_openlines, is_required=True)

        if skip_chat is not MISSING:
            params["SKIP_CHAT"] = bool_to_bitrix(skip_chat, is_required=True)

        if skip_dialog is not MISSING:
            params["SKIP_DIALOG"] = bool_to_bitrix(skip_dialog, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params or None,
            timeout=timeout,
        )
