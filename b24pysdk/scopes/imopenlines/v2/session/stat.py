from typing import Iterable, Text

from .....api.requests import BitrixAPIRequest
from .....utils.functional import classproperty, type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "Stat",
]


class Stat(BaseEntity):
    """Class for retrieving batch session metrics.

    Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/statistics/index.html
    """

    @classproperty
    def _name(cls) -> Text:
        return "Stat"

    @type_checker
    def get(
            self,
            session_id: Iterable[int],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get session metrics

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/statistics/imopenlines-v2-session-stat-get.html

        The method retrieves batch metrics for open channel sessions.

        Args:
            session_id: Array of session IDs;

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
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )
