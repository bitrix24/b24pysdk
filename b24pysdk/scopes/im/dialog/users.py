from typing import Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.converters import bool_to_bitrix
from ....utils.functional import type_checker
from ....utils.types import JSONList, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Users",
]


class Users(BaseEntity):
    """Class for retrieving chat participants.

    Documentation: https://apidocs.bitrix24.com/api-reference/chats/chat-users/index.html
    """

    @type_checker
    def list(
            self,
            dialog_id: Text,
            *,
            skip_external: Optional[bool] = MISSING,
            skip_external_except_types: Optional[Text] = MISSING,
            limit: Optional[int] = MISSING,
            last_id: Optional[int] = MISSING,
            offset: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONList]:
        """Get the list of participants

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/chat-users/im-dialog-users-list.html

        The method returns detailed information about the participants in the dialog with pagination support.

        Args:
            dialog_id: Chat identifier;

            skip_external: Exclude system users;

            skip_external_except_types: A list of types of system users to keep in the selection, separated by commas;

            limit: Number of items per page;

            last_id: Identifier of the last user from selection limit;

            offset: Offset for pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            DIALOG_ID=dialog_id,
        )

        if skip_external is not MISSING:
            params["SKIP_EXTERNAL"] = bool_to_bitrix(skip_external, is_required=True)

        if skip_external_except_types is not MISSING:
            params["SKIP_EXTERNAL_EXCEPT_TYPES"] = skip_external_except_types

        if limit is not MISSING:
            params["LIMIT"] = limit

        if last_id is not MISSING:
            params["LAST_ID"] = last_id

        if offset is not MISSING:
            params["OFFSET"] = offset

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
