from typing import Optional

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from .._base_crm import BaseCRM

__all__ = [
    "Delivery",
]


class Delivery(BaseCRM):
    """These methods offer capabilities for obtaining information about deliveries.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/delivery/index.html
    """

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get delivery information by ID.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/delivery/crm-item-delivery-get.html

        This method retrieves brief information about delivery.

        Args:
            bitrix_id: Delivery identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._get(bitrix_id, timeout=timeout)

    @type_checker
    def list(
            self,
            *,
            entity_type_id: int,
            entity_id: int,
            filter: Optional[JSONDict] = None,
            order: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get list of deliveries.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/delivery/crm-item-delivery-list.html

        Args:
            entity_type_id: Identifier of the crm object type;

            entity_id: Identifier of the crm object;

            filter: Object format:

                {
                    "field_1": "value_1",

                    "field_2": "value_2",

                    ...,

                    "field_n": "value_n",
                };

            order: Object format:

                {
                    field_1: value_1,

                    ...,
                }

                where

                - field_n is the name of the field by which the selection will be sorted

                - value_n is a string value equals to 'asc' (ascending sort) or 'desc' (descending sort);

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "entityTypeId": entity_type_id,
            "entityId": entity_id,
        }

        if filter is not None:
            params["filter"] = filter

        if order is not None:
            params["order"] = order

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
