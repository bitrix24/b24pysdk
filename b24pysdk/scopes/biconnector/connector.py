from typing import Iterable, Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from ._base_biconnector import BaseBiconnector

__all__ = [
    "Connector",
]


class Connector(BaseBiconnector):
    """
    Handle operations related to Bitrix24 BI Connector connectors.

    Documentation: https://apidocs.bitrix24.com/api-reference/biconnector/connector/index.html
    """

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve the description of connector fields.

        Documentation: https://apidocs.bitrix24.com/api-reference/biconnector/connector/biconnector-connector-fields.html

        This method returns meta information about the available fields of a connector.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """
        return super().fields(timeout=timeout)

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Create a new BI Connector.

        Documentation: https://apidocs.bitrix24.com/api-reference/biconnector/connector/biconnector-connector-add.html

        Creates a connector used to integrate external data sources with Bitrix24 BI Connector.

        Args:
            fields: Object format:
                {
                    "field_1": "value_1",

                    ...,

                    "field_n": "value_n",
                };

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """
        return super().add(fields, timeout=timeout)

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve information about a connector by its identifier.

        Documentation: https://apidocs.bitrix24.com/api-reference/biconnector/connector/biconnector-connector-get.html

        Returns details for the connector specified by the provided identifier.

        Args:
            bitrix_id: Identifier of the connector;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """
        return super().get(bitrix_id, timeout=timeout)

    @type_checker
    def list(
            self,
            *,
            select: Optional[Iterable[Text]] = None,
            filter: Optional[JSONDict] = None,
            order: Optional[JSONDict] = None,
            page: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve a list of connectors using selection criteria.

        Documentation: https://apidocs.bitrix24.com/api-reference/biconnector/connector/biconnector-connector-list.html

        Implements a list method for connectors. The set of returned fields can be adjusted with the select parameter.

        Args:
            select: List of field names to include in the result set; if omitted, all fields are returned;

            filter: Object format:
                {
                    "field_1": "value_1",

                    "field_2": "value_2",
                };

            order: Object format:
                {
                    "field_1": "ASC|DESC",

                    "field_2": "ASC|DESC",
                };

            page: Pagination control parameter;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """
        return super().list(select=select, filter=filter, order=order, page=page, timeout=timeout)

    @type_checker
    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Update an existing BI Connector.

        Documentation: https://apidocs.bitrix24.com/api-reference/biconnector/connector/biconnector-connector-update.html

        Applies the provided field values to the specified connector.

        Args:
            bitrix_id: Identifier of the connector to update;

            fields: Object format:
                {
                    "field_1": "value_1",

                    "field_2": "value_2",

                    ...,

                    "field_n": "value_n",
                };

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """
        return super().update(
            bitrix_id,
            fields,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Delete an existing connector by its identifier.

        Documentation: https://apidocs.bitrix24.com/api-reference/biconnector/connector/biconnector-connector-delete.html

        Removes the connector if it has no linked sources.

        Args:
            bitrix_id: Identifier of the connector to delete;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """
        return super().delete(bitrix_id, timeout=timeout)
