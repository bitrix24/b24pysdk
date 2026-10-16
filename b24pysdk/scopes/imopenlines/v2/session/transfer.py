from typing import Iterable, Text

from .....api.requests import BitrixAPIRequest
from .....utils.functional import classproperty, type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "Transfer",
]


class Transfer(BaseEntity):
    """Class for retrieving session transfer history.

    Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/statistics/index.html
    """

    @classproperty
    def _name(cls) -> Text:
        return "Transfer"

    @type_checker
    def list(
            self,
            session_id: Iterable[int],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get transfer history

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/statistics/imopenlines-v2-session-transfer-list.html

        The method retrieves transfer history for open channel session.

        Args:
            session_id: Array of sessions IDs;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if session_id.__class__ is not list:
            session_id = list(session_id)

        params: JSONDict = {
            "sessionId": session_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
