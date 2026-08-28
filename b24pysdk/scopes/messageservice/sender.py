from typing import List, Optional, Text, Union

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Sender",
]


class Sender(BaseEntity):
    """Class provides methods for working with message providers.

    Documentation: https://apidocs.bitrix24.com/api-reference/messageservice/index.html
    """

    @type_checker
    def add(
            self,
            code: Text,
            type: Text,
            handler: Text,
            name: Union[Text, JSONDict],
            *,
            description: Optional[Union[Text, JSONDict]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Register an SMS provider

        Documentation: https://apidocs.bitrix24.com/api-reference/messageservice/messageservice-sender-add.html

        The method registers a new message provider.

        Args:
            code: Provider code;

            type: Provider type;

            handler: Application handler URL that is called when sending a message;

            name: Provider name;

            description: Provider description;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "CODE": code,
            "TYPE": type,
            "HANDLER": handler,
            "NAME": name,
        }

        if description is not MISSING:
            params["DESCRIPTION"] = description

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            code: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Delete SMS provider

        Documentation: https://apidocs.bitrix24.com/api-reference/messageservice/messageservice-sender-delete.html

        The method removes a previously registered message provider for the current application.

        Args:
            code: Provider code;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "CODE": code,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[List[Text]]:
        """Get a list of SMS providers

        Documentation: https://apidocs.bitrix24.com/api-reference/messageservice/messageservice-sender-list.html

        The method returns a list of provider codes registered with the current application.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            code: Text,
            *,
            handler: Optional[Text] = MISSING,
            name: Optional[Union[Text, JSONDict]] = MISSING,
            description: Optional[Union[Text, JSONDict]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Updates an SMS provider

        The method updates an existing message provider.

        Args:
            code: Provider code;

            handler: Application handler URL that is called when sending a message;

            name: Provider name;

            description: Provider description;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "CODE": code,
        }

        if handler is not MISSING:
            params["HANDLER"] = handler

        if name is not MISSING:
            params["NAME"] = name

        if description is not MISSING:
            params["DESCRIPTION"] = description

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
