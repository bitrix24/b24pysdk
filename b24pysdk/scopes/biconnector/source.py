from typing import Iterable, Optional, Text

from ...bitrix_api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from ._base_biconnector import BaseBiconnector

__all__ = [
    "Source",
]


class Source(BaseBiconnector):
    """
    Handle operations related to Bitrix24 BIconnector sources.

    Documentation: https://apidocs.bitrix24.com/api-reference/biconnector/source/index.html
    """

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve the description of fields for a BIconnector source.

        Documentation: https://apidocs.bitrix24.com/api-reference/biconnector/source/biconnector-source-fields.html

        Args:
            timeout: Timeout in seconds;

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
        Create a new BIconnector source.

        Documentation: https://apidocs.bitrix24.com/api-reference/biconnector/source/biconnector-source-add.html

        Args:
            fields: Object format:
                {
                    "field_1": "value_1",

                    "field_2": "value_2",

                    ...,

                    "field_n": "value_n",
                };
            timeout: Timeout in seconds;

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
        Retrieve information about a BIconnector source by its identifier.

        Documentation: https://apidocs.bitrix24.com/api-reference/biconnector/source/biconnector-source-get.html

        Args:
            bitrix_id: Identifier of the source in Bitrix24;

            timeout: Timeout in seconds;

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
        Retrieve a list of BIconnector sources using optional filters and sorting.

        Documentation: https://apidocs.bitrix24.com/api-reference/biconnector/source/biconnector-source-list.html

        Args:
            select: Collection of field names to be returned in the result;
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

                    - value_n is a string value equals to 'ASC' (ascending sort) or 'DESC' (descending sort);

            page: Page number for paginated results;

            timeout: Timeout in seconds;

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
        Update an existing BIconnector source by its identifier.

        Documentation: https://apidocs.bitrix24.com/api-reference/biconnector/source/biconnector-source-update.html

        Args:
            bitrix_id: Identifier of the source in Bitrix24;
            fields: Object format:
                {
                    "field_1": "value_1",

                    "field_2": "value_2",

                    ...,

                    "field_n": "value_n",
                };
            timeout: Timeout in seconds;

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
        Delete an existing BIconnector source by its identifier.

        Documentation: https://apidocs.bitrix24.com/api-reference/biconnector/source/biconnector-source-delete.html

        Args:
            bitrix_id: Identifier of the source in Bitrix24;

            timeout: Timeout in seconds;

        Returns:
            Instance of BitrixAPIRequest.
        """
        return super().delete(bitrix_id, timeout=timeout)
