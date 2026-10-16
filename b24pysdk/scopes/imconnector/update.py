from typing import Iterable, Text, Union

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Update",
]


class Update(BaseEntity):
    """Class for modifying messages.

    Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/imconnector/index.html
    """

    @type_checker
    def messages(
            self,
            connector: Text,
            line: Union[int, Text],
            messages: Iterable[JSONDict],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update sent messages

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/imconnector/imconnector-update-messages.html

        The method updates the data of previously sent messages from an external system in an open line.

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
