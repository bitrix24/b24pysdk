from functools import cached_property
from typing import Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity
from .connector import Connector

__all__ = [
    "Sip",
]


class Sip(BaseEntity):
    """Class for managing SIP connections.

    Documentation: https://apidocs.bitrix24.com/api-reference/telephony/voximplant/sip/index.html
    """

    @cached_property
    def connector(self) -> Connector:
        """"""
        return Connector(self)

    @type_checker
    def add(
            self,
            type: Text,
            title: Text,
            server: Text,
            login: Text,
            password: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create SIP line

        Documentation: https://apidocs.bitrix24.com/api-reference/telephony/voximplant/sip/voximplant-sip-add.html

        The method creates a new SIP line associated with an application.

        Args:
            type: Type of PBX;

            title: Name of the connection;

            server: Address of the SIP registration server;

            login: Login for connecting to the server;

            password: Password for connecting to the server;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "TYPE": type,
            "TITLE": title,
            "SERVER": server,
            "LOGIN": login,
            "PASSWORD": password,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            config_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete SIP line

        Documentation: https://apidocs.bitrix24.com/api-reference/telephony/voximplant/sip/voximplant-sip-delete.html

        The method removes an existing SIP line created by the current application.

        Args:
            config_id: Identifier of the SIP line configuration;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "CONFIG_ID": config_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            *,
            filter: Optional[JSONDict] = MISSING,
            sort: Optional[Text] = MISSING,
            order: Optional[Text] = MISSING,
            start: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get SIP line of the application

        Documentation: https://apidocs.bitrix24.com/api-reference/telephony/voximplant/sip/voximplant-sip-get.html

        The method returns a list of SIP lines created by the current application.

        Args:
            filter: Object for filtering;

            sort: Sorting field;

            order: Sort direction;

            start: Pagination parameter;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if filter is not MISSING:
            params["FILTER"] = filter

        if sort is not MISSING:
            params["SORT"] = sort

        if order is not MISSING:
            params["ORDER"] = order

        if start is not MISSING:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def status(
            self,
            reg_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get SIP registration status

        Documentation: https://apidocs.bitrix24.com/api-reference/telephony/voximplant/sip/voximplant-sip-status.html

        The method returns the current SIP registration status for the cloud PBX.

        Args:
             reg_id: Identifier of the SIP registration;

             timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "REG_ID": reg_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.status,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            config_id: int,
            *,
            title: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update SIP line

        Documentation: https://apidocs.bitrix24.com/api-reference/telephony/voximplant/sip/voximplant-sip-update.html

        The method updates an existing SIP line created by the current application.

        Args:
            config_id: identifier of the SIP line configuration;

            title: The name for the connection;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "CONFIG_ID": config_id,
        }

        if title is not MISSING:
            params["TITLE"] = title

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
