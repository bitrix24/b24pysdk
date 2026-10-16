from functools import cached_property
from typing import Text

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity
from .message import Message

__all__ = [
    "Network",
]


class Network(BaseEntity):
    """Class for creating external open channels.

    Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/index.html
    """

    @cached_property
    def message(self) -> Message:
        """"""
        return Message(self)

    @type_checker
    def join(
            self,
            code: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Connect an external open channel to the account

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/imopenlines-network-join.html

        The method connects an external open channel from another Bitrix24 to the current Bitrix24.

        Args:
            code: The code of the open line channe; as a string of 32 characters;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            CODE=code,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.join,
            params=params,
            timeout=timeout,
        )
