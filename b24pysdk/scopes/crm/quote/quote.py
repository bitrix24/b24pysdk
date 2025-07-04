from typing import Iterable, Optional, Text

from ...._bitrix_api_request import BitrixAPIRequest
from ....utils.types import JSONDict
from .._productrows import Productrows
from .._userfield import Userfield
from ..item import Item


class Quote(Item):
    """An estimate is a CRM object that allows you to create printed documents and send them to the client before a deal.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/quote/index.html
    """

    ENTITY_TYPE_ID = 7
    ENTITY_TYPE_NAME = "QUOTE"
    ENTITY_TYPE_ABBR = "Q"
    USER_FIELD_ENTITY_ID = "CRM_QUOTE"

    def fields(
            self,
            *args,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Get fields of the estimate.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/quote/crm-quote-fields.html

        The method returns the description of fields for the estimate including custom fields.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return super().fields(entity_type_id=self.ENTITY_TYPE_ID, timeout=timeout)

    def add(
            self,
            fields: JSONDict,
            *args,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Create a new estimate.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/quote/crm-quote-add.html

        The method creates a new estimate.

        The created estimate must include the seller and buyer companies.

        Args:
            fields: Object format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
                }

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return super().add(
            fields,
            entity_type_id=self.ENTITY_TYPE_ID,
            timeout=timeout,
        )

    def get(
            self,
            bitrix_id: int,
            *args,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Get an estimate by ID.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/quote/crm-quote-get.html

        The method returns an estimate by its ID.

        Args:
            bitrix_id: Identifier of the estimate;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return super().get(
            bitrix_id,
            entity_type_id=self.ENTITY_TYPE_ID,
            timeout=timeout,
        )

    def list(
            self,
            *args,
            select: Optional[Iterable[Text]] = None,
            filter: Optional[JSONDict] = None,
            order: Optional[JSONDict] = None,
            start: Optional[int] = None,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Get list of estimates.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/quote/crm-quote-list.html

        The method returns a list of estimates by filter.

        Args:
            select: List of fields that should be populated for deals in the selection;

            filter: Object format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
                }

            order:  Object format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
                }

            start: This parameter is used to manage pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return super().list(
            entity_type_id=self.ENTITY_TYPE_ID,
            select=select,
            filter=filter,
            order=order,
            start=start,
            timeout=timeout,
        )

    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *args,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Update the estimate.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/quote/crm-quote-update.html

        The method updates an existing estimate.

        Args:
            bitrix_id: Identifier of the estimate;

            fields: Object format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
                }

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return super().update(
            bitrix_id,
            fields,
            entity_type_id=self.ENTITY_TYPE_ID,
            timeout=timeout,
        )

    def delete(
            self,
            bitrix_id: int,
            *args,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Delete estimate.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/quote/crm-quote-delete.html

        The method removes an estimate and all associated objects.

        Args:
            bitrix_id: Identifier of the estimate;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return super().delete(
            bitrix_id,
            entity_type_id=self.ENTITY_TYPE_ID,
            timeout=timeout,
        )

    @property
    def productrows(self) -> Productrows:
        """"""
        return Productrows(self)

    @property
    def userfield(self) -> Userfield:
        """"""
        return Userfield(self)
