from typing import Text, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Data",
]


class Data(BaseEntity):
    """Class for managing connector settings.

    Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/imconnector/index.html
    """

    @type_checker
    def set(
            self,
            connector: Text,
            line: Union[int, Text],
            data: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Set connector settings

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/imconnector/imconnector-connector-data-set.html

        The method sets the channel settings in an external system for a custom connector and specified open line.

        Args:
            connector: The string code of the connector;

            line: Identifier of the open line;

            data: Object containing the channel settings in the external system;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            CONNECTOR=connector,
            LINE=line,
            DATA=data,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.set,
            params=params,
            timeout=timeout,
        )
