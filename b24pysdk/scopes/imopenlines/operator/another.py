from typing import Text, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Another",
]


class Another(BaseEntity):
    """Class for completing another's dialogue.

    Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/operators/index.html
    """

    @type_checker
    def finish(
            self,
            chat_id: Union[int, Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Finish another operator's dialog

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/operators/imopenlines-operator-another-finish.html

        The method ends a dialog in an open line, even if dialog is assigned to another operator.

        Args:
            chat_id: Identifier of the open line chat;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            CHAT_ID=chat_id,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.finish,
            params=params,
            timeout=timeout,
        )
