from typing import Iterable, Optional

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Fields",
]


class Fields(BaseEntity):
    """Methods for biconnector.dataset.fields.* endpoints."""

    @type_checker
    def __call__(
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
        return self._make_bitrix_api_request(
            api_wrapper=self,
            timeout=timeout,
        )

    @type_checker
    def update(
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
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
