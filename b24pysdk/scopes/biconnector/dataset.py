from typing import Iterable, Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from ._base_biconnector import BaseBiconnector

__all__ = [
    "Dataset",
]


class Dataset(BaseBiconnector):
    """Handle operations related to Bitrix24 BIconnector datasets.

    Documentation: https://apidocs.bitrix24.com/api-reference/biconnector/dataset/index.html
    """

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve a description of dataset fields.

        Documentation: https://apidocs.bitrix24.com/api-reference/biconnector/dataset/biconnector-dataset-fields.html

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
        Create a new dataset linked to a data source.

        Documentation: https://apidocs.bitrix24.com/api-reference/biconnector/dataset/biconnector-dataset-add.html

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
        Retrieve information about a dataset by its identifier.

        Documentation: https://apidocs.bitrix24.com/api-reference/biconnector/dataset/biconnector-dataset-get.html

        Args:
            bitrix_id: Dataset identifier;

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
        Return a list of datasets by filter.

        Documentation: https://apidocs.bitrix24.com/api-reference/biconnector/dataset/biconnector-dataset-list.html

        Args:
            select: List of fields to be included for datasets in the selection. By default, all fields are returned. The field "fields" is not supported and will be ignored;

            filter: Object format:
                {
                    "field_1": "value_1",

                    "field_2": "value_2",
                    ...
                };

            order: Ordering options;

            page: Page number;

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
        Update an existing dataset.

        Documentation: https://apidocs.bitrix24.com/api-reference/biconnector/dataset/biconnector-dataset-update.html

        Args:
            bitrix_id: Dataset identifier;

            fields: Object format:
                {
                    "description": "string"
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
        Delete an existing dataset.

        Documentation: https://apidocs.bitrix24.com/api-reference/biconnector/dataset/biconnector-dataset-delete.html

        Args:
            bitrix_id: Dataset identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """
        return super().delete(bitrix_id, timeout=timeout)

    @type_checker
    def fields_update(
            self,
            bitrix_id: int,
            add: Optional[Iterable[JSONDict]] = None,
            update: Optional[Iterable[JSONDict]] = None,
            delete: Optional[Iterable[int]] = None,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Update fields of an existing dataset.

        Documentation: https://apidocs.bitrix24.com/api-reference/biconnector/dataset/biconnector-dataset-fields-update.html

        Args:
            bitrix_id: Dataset identifier;

            add: List of new fields to add. Object format:
                [
                    { "type": "int", "name": "NAME", "externalCode": "NAME" },
                    ...
                ];

            update: List of fields to update. Object format:
                [
                    { "id": 12, "visible": false },
                    ...
                ];

            delete: List of field identifiers to delete.

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {"id": bitrix_id}

        if add is not None:
            params["add"] = list(add)

        if update is not None:
            params["update"] = list(update)

        if delete is not None:
            params["delete"] = list(delete)

        return self._make_bitrix_api_request(
            api_wrapper=self.fields_update,
            params=params,
            timeout=timeout,
        )
