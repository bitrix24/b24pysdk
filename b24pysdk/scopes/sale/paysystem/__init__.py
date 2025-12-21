from functools import cached_property
from typing import Text, Optional, Union

from ..._base_scope import BaseScope
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout, B24BoolStrict
from ....bitrix_api.requests import BitrixAPIRequest
from .handler import Handler
from .settings import Settings

_all__ = [
    "Paysystem",
]


class Paysystem(BaseScope):
    @cached_property
    def handler(self) -> Handler:
        """"""
        return Handler(self)

    @cached_property
    def settings(self) -> Settings:
        """"""
        return Settings(self)

    @type_checker
    def list(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        The method returns a list of payment systems

        Documentation: https://apidocs.bitrix24.com/api-reference/pay-system/sale-pay-system-list.html

        Args:

            timeout: Timeout for the request in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            sale_paysystem_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        This method updates the payment system

        Documentation: https://apidocs.bitrix24.com/api-reference/pay-system/sale-pay-system-delete.html

        Args:
            sale_paysystem_id: Payment system ID

            timeout: Timeout for the request in seconds.
        Returns:
            BitrixAPIRequest object for the API call
        """

        params = {
            "ID": sale_paysystem_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            sale_paysystem_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        This method updates the payment system

        Documentation: https://apidocs.bitrix24.com/api-reference/pay-system/sale-pay-system-update.html

        Args:
            sale_paysystem_id: Payment system ID

            fields: Object containing new field values. See documentation for details.

            timeout: Timeout for the request in seconds.

        Returns:
            BitrixAPIRequest object for the API call
        """

        params = {
            "ID": sale_paysystem_id,
            "FIELDS": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def add(
            self,
            name: Text,
            person_type_id: int,
            bx_rest_handler: Text,
            entity_register_type: Text,
            ps_settings: JSONDict,
            *,
            description: Optional[Text] = None,
            timeout: Timeout = None,
            logotype: Optional[Text] = None,
            new_window: Optional[Union[bool, B24BoolStrict]] = None,
            xml_id: Optional[Text] = None,
            active: Optional[Union[bool, B24BoolStrict]] = None,
    ) -> BitrixAPIRequest:
        """
        This method adds a payment system.

        Documentation: https://apidocs.bitrix24.com/api-reference/pay-system/sale-pay-system-add.html

        Args:
            name: Name of the payment system

            person_type_id: Identifier of the payer type

            bx_rest_handler: Code of the REST handler specified when adding the handler using the method sale.paysystem.handler.add

            entity_register_type: Binding of the payment system:
                ORDER — value for store orders, deals, smart processes
                CRM_INVOICE — value for CRM invoices
                CRM_QUOTE — value for CRM estimates

            ps_settings: List of handler settings values in the format {"field_1": "value_1", ... "field_N": "value_N"}, where field is the name of the setting, and value is an object containing keys TYPE and VALUE (see description below).
                         The structure of the settings is defined when adding the payment system handler in the method sale.paysystem.handler.add under the CODES key of the SETTINGS parameter

            description: Description of the payment system

            timeout: Timeout for the request in seconds.

            logotype: Logo of the payment system (image in Base64 format)

            new_window: Flag for the setting "Open in new window".

            xml_id: External identifier of the payment system. Can be used as an additional parameter for filtering in sale.paysystem.list

            active: Indicator of the payment system's activity. Possible values:

        Returns:
            BitrixAPIRequest object for the API call
        """

        params = {
            "NAME": name,
            "SETTINGS": ps_settings,
            "BX_REST_HANDLER": bx_rest_handler,
            "PERSON_TYPE_ID": person_type_id,
            "ENTITY_REGISTRY_TYPE": entity_register_type,
        }

        if new_window is not None:
            params["NEW_WINDOW"] = B24BoolStrict(new_window).to_b24()

        if active is not None:
            params["ACTIVE"] = B24BoolStrict(active).to_b24()

        if description is not None:
            params["DESCRIPTION"] = description

        if logotype is not None:
            params["LOGOTYPE"] = logotype

        if xml_id is not None:
            params["XML_ID"] = xml_id

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )
