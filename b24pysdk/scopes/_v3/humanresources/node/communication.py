from typing import Iterable, Optional, Text

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "Communication",
]


class Communication(BaseEntity):
    """Methods for managing departments and teams communication.

    Documentation: https://apidocs.bitrix24.com/api-reference/departments/node-communication/index.html
    """

    @type_checker
    def edit(
            self,
            node_id: int,
            communication_type: Text,
            *,
            ids: Optional[Iterable[int]] = MISSING,
            remove_ids: Optional[Iterable[int]] = MISSING,
            create_default: Optional[bool] = MISSING,
            with_children: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Edit communications

        Documentation: https://apidocs.bitrix24.com/api-reference/departments/node-communication/humanresources-node-communication-edit.html

        The method binds, unbinds, or creates a chat, channel, or collab for a department or team.

        Args:
            node_id: Identifier of the department or team;

            communication_type: Type of communication;

            ids: Identifiers of communications to be bound;

            remove_ids: Identifiers of communications to be unbound;

            create_default: Creates a default communication for the department or team;

            with_children: Applies the change to child department and teams;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "nodeId": node_id,
            "communicationType": communication_type,
        }

        if ids is not MISSING:
            if ids.__class__ is not list:
                ids = list(ids)

            params["ids"] = ids

        if remove_ids is not MISSING:
            if remove_ids.__class__ is not list:
                remove_ids = list(remove_ids)

            params["removeIds"] = remove_ids

        if create_default is not MISSING:
            params["createDefault"] = create_default

        if with_children is not MISSING:
            params["withChildren"] = with_children

        return self._make_bitrix_api_request(
            api_wrapper=self.edit,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get communications

        Documentation: https://apidocs.bitrix24.com/api-reference/departments/node-communication/humanresources-node-communication-list.html

        The method returns chats, channels, and collabs associated with a department or team.

        Args:
            bitrix_id: Identifier of the department or team;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
