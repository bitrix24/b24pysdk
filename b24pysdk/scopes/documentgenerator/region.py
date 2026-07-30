from typing import Optional, Text, Union

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Region",
]


class Region(BaseEntity):
    """Class helps handle local settings for document generator numerators.

    Documentation: https://apidocs.bitrix24.com/api-reference/document-generator/region/index.html
    """

    @type_checker
    def add(
        self,
        fields: JSONDict,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add region

        Documentation: https://apidocs.bitrix24.com/api-reference/document-generator/region/document-generator-region-add.html

        The method adds a new custom region.

        Args:
            fields: Region parameters;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
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
        bitrix_id: Union[int, Text],
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete region

        Documentation: https://apidocs.bitrix24.com/api-reference/document-generator/region/document-generator-region-delete.html

        The method removes a custom region by its identifier.

        Args:
            bitrix_id: Region identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
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
        bitrix_id: Union[int, Text],
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get region by ID

        Documentation: https://apidocs.bitrix24.com/api-reference/document-generator/region/document-generator-region-get.html

        The method returns region data based on the identifier or code.

        Args:
            bitrix_id: Region identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
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
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of regions

        Documentation: https://apidocs.bitrix24.com/api-reference/document-generator/region/document-generator-region-list.html

        The method returns a list of pre-installed and custom regions.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            timeout=timeout,
        )

    @type_checker
    def update(
        self,
        bitrix_id: Union[int, Text],
        *,
        fields: Optional[JSONDict] = MISSING,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update region

        Documentation: https://apidocs.bitrix24.com/api-reference/document-generator/region/document-generator-region-update.html

        The method updates a user-defined region by its identifier.

        Args:
            bitrix_id: Region identifier;

            fields: New region parameters;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        if fields is not MISSING:
            params["fields"] = fields

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
