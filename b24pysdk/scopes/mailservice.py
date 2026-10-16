from typing import Optional, Sequence, Text, Union

from .._constants import MISSING
from ..api.requests import BitrixAPIRequest
from ..utils.converters import bool_to_bitrix
from ..utils.functional import type_checker
from ..utils.types import B24File, Timeout
from ._base_scope import BaseScope

__all__ = [
    "Mailservice",
]


class Mailservice(BaseScope):
    """Class for managing mail service.

    Documentation: https://apidocs.bitrix24.com/api-reference/mailservice/index.html
    """

    @type_checker
    def add(
            self,
            name: Text,
            encryption: bool,
            *,
            active: Optional[bool] = MISSING,
            server: Optional[Text] = MISSING,
            port: Optional[int] = MISSING,
            link: Optional[Text] = MISSING,
            sort: Optional[int] = MISSING,
            icon: Optional[Union[int, Text, Sequence[Text]]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create mail service

        Documentation: https://apidocs.bitrix24.com/api-reference/mailservice/mailservice-add.html

        The method creates a mail service for the current Bitrix24.

        Args:
            name: Name of the mail service;

            encryption: Secure connection status;

            active: Service activity status;

            server: IMAP server address;

            port: IMAP server port;

            link: Web interface address of the mail service;

            sort: Sort index;

            icon: Service logo;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "NAME": name,
            "ENCRYPTION": bool_to_bitrix(encryption),
        }

        if active is not MISSING:
            params["ACTIVE"] = bool_to_bitrix(active)

        if server is not MISSING:
            params["SERVER"] = server

        if port is not MISSING:
            params["PORT"] = port

        if link is not MISSING:
            params["LINK"] = link

        if sort is not MISSING:
            params["SORT"] = sort

        if icon is not MISSING:
            params["ICON"] = icon

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete mail service

        Documentation: https://apidocs.bitrix24.com/api-reference/mailservice/mailservice-delete.html

        The method removes a mail service by its identifier.

        Args:
            bitrix_id: Identifier od the mail service;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "ID": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get mail service fields

        Documentation: https://apidocs.bitrix24.com/api-reference/mailservice/mailservice-fields.html

        The method returns localized names of the mail service fields.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.fields,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the mail service

        Documentation: https://apidocs.bitrix24.com/api-reference/mailservice/mailservice-get.html

        The method returns the parameters of the mail service by its identifier.

        Args:
            bitrix_id: Identifier of the mail service;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "ID": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of mail services

        Documentation: https://apidocs.bitrix24.com/api-reference/mailservice/mailservice-list.html

        The method returns a list of active mail services.

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
            bitrix_id: int,
            *,
            active: Optional[bool] = MISSING,
            name: Optional[Text] = MISSING,
            server: Optional[Text] = MISSING,
            port: Optional[int] = MISSING,
            encryption: Optional[bool] = MISSING,
            link: Optional[Text] = MISSING,
            sort: Optional[int] = MISSING,
            icon: Optional[Union[int, Text, Sequence[Text]]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update mail service

        Documentation: https://apidocs.bitrix24.com/api-reference/mailservice/mailservice-update.html

        The method modifies the parameters of an existing mail service.

        Args:
            bitrix_id: Identifier of the mail service;

            active: Service activity status;

            name: Name of the mail service;

            server: IMAP server address;

            port: IMAP server port;

            encryption: Secure connection status;

            link: Web interface address of the mail service;

            sort: Sort index;

            icon: Service logo;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "ID": bitrix_id,
        }

        if active is not MISSING:
            params["ACTIVE"] = bool_to_bitrix(active)

        if name is not MISSING:
            params["NAME"] = name

        if server is not MISSING:
            params["SERVER"] = server

        if port is not MISSING:
            params["PORT"] = port

        if encryption is not MISSING:
            params["ENCRYPTION"] = bool_to_bitrix(encryption)

        if link is not MISSING:
            params["LINK"] = link

        if sort is not MISSING:
            params["SORT"] = sort

        if icon is not MISSING:
            if isinstance(icon, (int, Text)):
                params["ICON"] = icon
            else:
                params["ICON"] = B24File(icon).to_b24()

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
