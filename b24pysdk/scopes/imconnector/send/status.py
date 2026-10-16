from typing import Iterable, Text, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Status",
]


class Status(BaseEntity):
    """Class for transferring external channel messages to Bitrix24.

    Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/imconnector/index.html
    """

    @type_checker
    def delivery(
            self,
            connector: Text,
            line: Union[int, Text],
            messages: Iterable[JSONDict],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update status 'Delivered'

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/imconnector/imconnector-send-status-delivery.html

        The method confirms in Bitrix24 that an outgoing message from an open line has been successfully delivered to an external system.

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
            api_wrapper=self.delivery,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def reading(
            self,
            connector: Text,
            line: Union[int, Text],
            messages: Iterable[JSONDict],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Check 'Read' status

        The method confirms in Bitrix24 that an outgoing message from an open line has been read.

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
            api_wrapper=self.reading,
            params=params,
            timeout=timeout,
        )
