from typing import Iterable, Optional, Text

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from .._base_crm import BaseCRM

__all__ = [
    "Link",
]


class Link(BaseCRM):
    """The methods provide capabilities for managing links between requisites and CRM objects.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/requisites/links/index.html
    """

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get description of CRM requisite.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/requisites/links/crm-requisite-link-fields.html

        The method returns a formal description of the link fields for requisites.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._fields(timeout=timeout)

    @type_checker
    def get(
            self,
            *,
            entity_type_id: int,
            entity_id: int,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get requisite link with CRM object.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/requisites/links/crm-requisite-link-get.html

        The method returns the link between requisites and an object.

        Args:
            entity_type_id: Identifier of the object type to which the link belongs, where possible values are:

                - deal (value 2),

                - old invoice (value 5),

                - estimate (value 7),

                - new invoice (value 31),

                - other dynamic objects;

            entity_id: Identifier of the object to which the link belongs;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "entityTypeId": entity_type_id,
            "entityId": entity_id,
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
            select: Optional[Iterable[Text]] = None,
            filter: Optional[JSONDict] = None,
            order: Optional[JSONDict] = None,
            start: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of requisite links.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/requisites/links/crm-requisite-link-list.html

        The method returns a list of requisite links based on the filter.

        Args:
            select: An array of fields to select;

            filter: Object format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
                };

            order: Object format:

                {
                    field_1: value_1,

                    ...,
                }

                where

                - field_n is the name of the field by which the selection will be sorted

                - value_n is a string value equals to 'asc' (ascending sort) or 'desc' (descending sort);

            start: This parameter is used for pagination control;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._list(
            select=select,
            filter=filter,
            order=order,
            start=start,
            timeout=timeout,
        )

    @type_checker
    def register(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Register requisite link.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/requisites/links/crm-requisite-link-register.html

        This method registers a link between requisites and an object.

        Args:
            fields: Object format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
                };

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.register,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unregister(
            self,
            *,
            entity_type_id: int,
            entity_id: int,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Unlink requisite from object.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/requisites/links/crm-requisite-link-unregister.html

        This method removes the link between requisites and an object.

        Args:
            entity_type_id: Identifier of the object type to which the link belongs, where possible values are:

                - deal (value 2),

                - old invoice (value 5),

                - estimate (value 7),

                - new invoice (value 31),

                - other dynamic objects;

            entity_id: Identifier of the object to which the link belongs;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "entityTypeId": entity_type_id,
            "entityId": entity_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.unregister,
            params=params,
            timeout=timeout,
        )
