from typing import Iterable, Optional, Sequence, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import classproperty, type_checker
from ...utils.types import B24File, JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "ProductImage",
]


class ProductImage(BaseEntity):
    """Handle operations related to Bitrix24 catalog product images.

    Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product-image/index.html
    """

    @classproperty
    def _name(cls) -> Text:
        return "productImage"

    @type_checker
    def add(
            self,
            fields: JSONDict,
            file_content: Sequence[Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add an image to a product, parent product (SKU), variation, or service.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product-image/catalog-product-image-add.html

        This method adds images to a product, parent product, variation, or service.

        Args:
            fields: Object format:
                {
                    "productId": Identifier of the product, parent product (SKU), variation, or service;

                    "type": Image type: 'DETAIL_PICTURE', 'PREVIEW_PICTURE', or 'MORE_PHOTO';
                };

            file_content: Array format:
                [
                    "file name",

                    "file content in base64",
                ];

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "fields": fields,
            "fileContent": B24File(file_content).to_b24(),
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            product_id: int,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete a product image by product and image identifiers.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product-image/catalog-product-image-delete.html

        This method removes an image from a product, parent product, variation, or service.

        Args:
            product_id: Identifier of the product, parent product (SKU), variation, or service;

            bitrix_id: Identifier of the product image;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "productId": product_id,
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
            product_id: int,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Retrieve information about a specific product image.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product-image/catalog-product-image-get.html

        This method returns information about a specific product image, main product, variation, or service.

        Args:
            product_id: Identifier of the product, parent product (SKU), variation, or service;

            bitrix_id: Identifier of the product image;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "productId": product_id,
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Retrieve available fields of the product image entity.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product-image/catalog-product-image-get-fields.html

        This method returns the available fields for a product image, main product, variation, or service.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.get_fields,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            product_id: int,
            *,
            select: Optional[Iterable[Text]] = MISSING,
            start: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of product images.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product-image/catalog-product-image-list.html

        The method returns a list of product images, parent product images, variations, or services.

        Args:
            product_id: Identifier of the product, parent product (SKU), variation, or service;

            select: Iterable with field names to return for each image;

            start: Start position for fetching the next page of results;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "productId": product_id,
        }

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        if start is not MISSING:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
