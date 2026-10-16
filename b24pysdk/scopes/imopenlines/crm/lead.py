from typing import Text, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Lead",
]


class Lead(BaseEntity):
    """Class for creating CRM leads based on a dialog.

    Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/index.html
    """

    @type_checker
    def create(
            self,
            chat_id: Union[int, Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create a lead based on the dialogue

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/sessions/imopenlines-crm-lead-create.html

        The method creates a CRM lead based on the current chat in the open channels.

        Args:
            chat_id: Identifier of the open channels chat;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            CHAT_ID=chat_id,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.create,
            params=params,
            timeout=timeout,
        )
