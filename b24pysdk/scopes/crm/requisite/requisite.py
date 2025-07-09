from typing import Iterable, Optional, Text

from ....bitrix_api.classes import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from .._userfield import Userfield
from ..item import Item
from .detail import Bankdetail, Preset
from .link import Link


class Requisite(Item):
    """
    Details are separate CRM entities that store data used in closing deals: Tax Identification Number (TIN),
    Tax Registration Reason Code (TRRC), Primary State Registration Number (PSRN), banking details, and addresses.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/requisites/index.html
    """

    ENTITY_TYPE_ID = 8
    ENTITY_TYPE_NAME = "REQUISITE"
    ENTITY_TYPE_ABBR = "RQ"
    USER_FIELD_ENTITY_ID = "CRM_REQUISITE"

    @property
    def bankdetail(self) -> Bankdetail:
        """"""
        return Bankdetail(self)

    @property
    def link(self) -> Link:
        """"""
        return Link(self)

    @property
    def preset(self) -> Preset:
        """"""
        return Preset(self)

    @property
    def userfield(self) -> Userfield:
        """"""
        return Userfield(self)

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get requisite fields.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/requisites/universal/crm-requisite-fields.html

        This method retrieves the description of the requisite fields.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._fields(timeout=timeout)

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add Requisite.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/requisites/universal/crm-requisite-add.html

        This method adds a new requisite.

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
        return self._add(fields, timeout=timeout)

    @type_checker
    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update Requisite.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/requisites/universal/crm-requisite-update.html

        This method updates an existing requisite.

        Args:
            bitrix_id: Identifier of the requisite.

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
        return self._update(
            bitrix_id,
            fields,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get requisite by ID.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/requisites/universal/crm-requisite-get.html

        This method retrieves a requisite by its identifier.

        Args:
            bitrix_id: Identifier of the requisite.

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._get(bitrix_id, timeout=timeout)

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
        """Get a list of requisites.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/requisites/universal/crm-requisite-list.html

        This method retrieves a list of requisites based on a filter.

        Args:
            select: An array containing the list of fields to be selected;

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

                - field_n is the name of the field by which the selection will be sorted,

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
    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete requisite.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/requisites/universal/crm-requisite-delete.html

        This method deletes a requisite and all related objects.

        Args:
            bitrix_id: Identifier of the requisite.

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._delete(bitrix_id, timeout=timeout)
