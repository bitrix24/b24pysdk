from typing import Optional, Text

from ....api.requests import BitrixAPIRequest
from ....utils.functional import classproperty, type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "ResourceType",
]


class ResourceType(BaseEntity):
    """Handle operations related to Bitrix24 booking resource types.

    Documentation: https://apidocs.bitrix24.com/api-reference/booking/resource/resource-type/index.html
    """

    @classproperty
    def _name(cls) -> Text:
        return "resourceType"

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Create a new resource type.

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/resource/resource-type/booking-v1-resourcetype-add.html

        This method sends the provided fields to create a resource type entity in the Booking module.

        Args:
            fields: Object format:
                {
                    "field_n": value_n,

                    "field_n": value_n,

                    ...
                };

                where
                    - field_n — field of the resource type for creating;
                    - value_n — field value;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "fields": fields,
        }

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
        """Delete a resource type by its identifier.

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/resource/resource-type/booking-v1-resourcetype-delete.html

        This method removes the specified resource type.

        Args:
            bitrix_id: Identifier of the resource type to delete;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
"""
        params = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve information about a resource type by its identifier.

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/resource/resource-type/booking-v1-resourcetype-get.html

        This method fetches the resource type details using its id.

        Args:
            bitrix_id: Identifier of the resource type to retrieve;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "id": bitrix_id,
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
            filter: Optional[JSONDict] = None,
            order: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve a list of resource types using optional filter and order.

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/resource/resource-type/booking-v1-resourcetype-list.html

        This method returns a filtered and/or ordered list of resource types. Use either searchQuery for substring search or name for exact name match. Default sorting is {ID: 'ASC'}.

        Args:
            filter: Object format:
                {
                    "field_n": value_n,

                    "field_n": value_n,

                    ...
                }

                where
                    - field_n — field of the resource type for filtering;
                    - value_n — field value;

            order: Object format:
                {
                    id: 'ASC' | 'DESC',

                    name: 'ASC' | 'DESC',

                    code: 'ASC' | 'DESC',
                };

                where

                - id — sort by identifier; value is 'ASC' (ascending) or 'DESC' (descending);
                - name — sort by name; value is 'ASC' or 'DESC';
                - code — sort by code; value is 'ASC' or 'DESC';

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = dict()

        if filter is not None:
            params["filter"] = filter

        if order is not None:
            params["order"] = order

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
        """
        Update an existing resource type.

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/resource/resource-type/booking-v1-resourcetype-update.html

        This method updates the fields of a resource type specified by its identifier.

        Args:
            bitrix_id: Identifier of the resource type to update;

            fields: Object format:
                {
                    "field_n": value_n,

                    "field_n": value_n,

                    ...
                };

                where
                    - field_n — field of the resource type for updating;
                    - value_n — field value;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "id": bitrix_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
