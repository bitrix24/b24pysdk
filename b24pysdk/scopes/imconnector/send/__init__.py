from functools import cached_property
from typing import Iterable, Text, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity
from .status import Status

__all__ = [
    "Send",
]


class Send(BaseEntity):
    """Class for transferring external channel messages to Bitrix24.

    Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/imconnector/index.html
    """

    @cached_property
    def status(self) -> Status:
        """"""
        return Status(self)

    @type_checker
    def messages(
            self,
            connector: Text,
            line: Union[int, Text],
            messages: Iterable[JSONDict],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Send messages to Bitrix24

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/imconnector/imconnector-send-messages.html

        The method accepts messages from an external system and forwards them to an open line in Bitrix24 via a custom connector.

        Args:
            connector: The string code of the connector;

            line: Identifier of the open line;

            messages: An array of messages;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if messages.__class__ is not list:
            messages = list(messages)

        params = dict(
            CONNECTOR=connector,
            LINE=line,
            MESSAGES=messages,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.messages,
            params=params,
            timeout=timeout,
        )
