from typing import Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.converters import bool_to_bitrix
from ....utils.functional import type_checker
from ....utils.types import JSONDict, JSONList, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Request",
]


class Request(BaseEntity):
    """Class for working with delivery requests.

    Documentation: https://apidocs.bitrix24.com/api-reference/sale/delivery/delivery-request/index.html
    """

    @type_checker
    def update(
        self,
        delivery_id: int,
        request_id: Text,
        *,
        finalize: Optional[bool] = MISSING,
        status: Optional[JSONDict] = MISSING,
        properties: Optional[JSONList] = MISSING,
        overwrite_properties: Optional[bool] = MISSING,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update delivery request

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/delivery/delivery-request/sale-delivery-request-update.html

        The method updates the delivery request.

        Args:
            delivery_id: Identifier of the delivery service to which delivery request belongs;

            request_id: Identifier of the delivery request;

            finalize: Indicator of the need to finalize the delivery request;

            status: Status of the delivery request;

            properties: Properties of the delivery request;

            overwrite_properties: Indicator of the need to completely overwrite the property values of the request during the update;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "DELIVERY_ID": delivery_id,
            "REQUEST_ID": request_id,
        }

        if finalize is not MISSING:
            params["FINALIZE"] = bool_to_bitrix(finalize, is_required=True)

        if status is not MISSING:
            params["STATUS"] = status

        if properties is not MISSING:
            params["PROPERTIES"] = properties

        if overwrite_properties is not MISSING:
            params["OVERWRITE_PROPERTIES"] = bool_to_bitrix(overwrite_properties, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def sendmessage(
        self,
        delivery_id: int,
        request_id: Text,
        addressee: Text,
        message: JSONDict,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create notifications for delivery request

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/delivery/delivery-request/sale-delivery-request-send-message.html

        The method creates notifications for a delivery request.

        Args:
            delivery_id: Identifier of the delivery service related to the delivery request;

            request_id: Identifier of the delivery request;

            addressee: Recipient of the message;

            message: Message;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "DELIVERY_ID": delivery_id,
            "REQUEST_ID": request_id,
            "ADDRESSEE": addressee,
            "MESSAGE": message,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.sendmessage,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
        self,
        delivery_id: int,
        request_id: Text,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete delivery request

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/delivery/delivery-request/sale-delivery-request-delete.html

        The method deletes a delivery request.

        Args:
            delivery_id: Identifier of the delivery service to which the delivery request belongs;

            request_id: Identifier of the delivery request;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "DELIVERY_ID": delivery_id,
            "REQUEST_ID": request_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )
