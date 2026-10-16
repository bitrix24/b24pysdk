from functools import cached_property
from typing import Iterable, Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.converters import bool_to_bitrix
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity
from .check import Check
from .handler import Handler

__all__ = [
    "Cashbox",
]


class Cashbox(BaseEntity):
    """Class for managing cash registers.

    Documentation: https://apidocs.bitrix24.com/api-reference/sale/cashbox/index.html
    """

    @cached_property
    def check(self) -> Check:
        """"""
        return Check(self)

    @cached_property
    def handler(self) -> Handler:
        """"""
        return Handler(self)

    @type_checker
    def add(
        self,
        name: Text,
        rest_code: Text,
        email: Text,
        *,
        ofd: Optional[Text] = MISSING,
        ofd_settings: Optional[JSONDict] = MISSING,
        number_kkm: Optional[Text] = MISSING,
        active: Optional[bool] = MISSING,
        sort: Optional[int] = MISSING,
        use_offline: Optional[bool] = MISSING,
        settings: Optional[JSONDict] = MISSING,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add cash register

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/cashbox/sale-cashbox-add.html

        The method adds a cash register.

        Args:
            name: Name of the cash register;

            rest_code: REST handler code for the cash register;

            email: Email address to which notifications will be sent in case of errors during receipt printing;

            ofd: OFD handler code;

            ofd_settings: OFD settings;

            number_kkm: External identifier of the cash register;

            active: Activity status of the cash register;

            sort: Sorting;

            use_offline: Whether the cash register is used offline;

            settings: Cash register settings;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "NAME": name,
            "REST_CODE": rest_code,
            "EMAIL": email,
        }

        if ofd is not MISSING:
            params["OFD"] = ofd

        if ofd_settings is not MISSING:
            params["OFD_SETTINGS"] = ofd_settings

        if number_kkm is not MISSING:
            params["NUMBER_KKM"] = number_kkm

        if active is not MISSING:
            params["ACTIVE"] = bool_to_bitrix(active, is_required=True)

        if sort is not MISSING:
            params["SORT"] = sort

        if use_offline is not MISSING:
            params["USE_OFFLINE"] = bool_to_bitrix(use_offline, is_required=True)

        if settings is not MISSING:
            params["SETTINGS"] = settings

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
        """Delete cash register

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/cashbox/sale-cashbox-delete.html

        The method deletes a cash register.

        Args:
            bitrix_id: Identifier of the cash register to be deleted;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "ID": bitrix_id,
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
        select: Optional[Iterable[Text]] = MISSING,
        filter: Optional[JSONDict] = MISSING,
        order: Optional[JSONDict] = MISSING,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of configured cash registers

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/cashbox/sale-cashbox-list.html

        The method retrieves a list of configured cash registers.

        Args:
            select: An array with the list of fields to select;

            filter: An object for filtering selected cash registers;

            order: An object for sorting selected records;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)
            params["SELECT"] = select

        if filter is not MISSING:
            params["FILTER"] = filter

        if order is not MISSING:
            params["ORDER"] = order

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
        self,
        bitrix_id: int,
        fields: JSONDict,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update existing cash register

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/cashbox/sale-cashbox-update.html

        The method updates an existing cash register.

        Args:
            bitrix_id: Identifier of the cash register being updated;

            fields: Values of the fields to be updated;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "ID": bitrix_id,
            "FIELDS": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
