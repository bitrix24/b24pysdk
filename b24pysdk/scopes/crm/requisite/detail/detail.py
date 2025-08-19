from abc import ABC
from typing import TYPE_CHECKING, Iterable, Optional, Text

from .....bitrix_api.classes import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...base_crm import BaseCRM

if TYPE_CHECKING:
    from ..requisite import Requisite


class Detail(BaseCRM, ABC):
    """The methods provide capabilities for managing requisite templates and bank details.

    Documentation:
    https://apidocs.bitrix24.com/api-reference/crm/requisites/presets/index.html
    https://apidocs.bitrix24.com/api-reference/crm/requisites/bank-detail/index.html
    """

    def __init__(self, requisite: "Requisite"):
        super().__init__(requisite._scope)
        self._path = self._get_path(requisite)

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get description of the entity fields.

        Documentation:
        https://apidocs.bitrix24.com/api-reference/crm/requisites/presets/crm-requisite-preset-fields.html
        https://apidocs.bitrix24.com/api-reference/crm/requisites/bank-detail/crm-requisite-bank-detail-fields.html

        The method returns a formal description of the fields of the requisite template or bank details.

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
        """Create a new entity.

        Documentation:
        https://apidocs.bitrix24.com/api-reference/crm/requisites/presets/crm-requisite-preset-add.html
        https://apidocs.bitrix24.com/api-reference/crm/requisites/bank-detail/crm-requisite-bank-detail-add.html

        This method creates a new requisites template or bank details.

        Args:
            fields: A set of fields - an object for adding a new entity;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._add(fields=fields, timeout=timeout)

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Get entity by ID.

        Documentation:
        https://apidocs.bitrix24.com/api-reference/crm/requisites/presets/crm-requisite-preset-get.html
        https://apidocs.bitrix24.com/api-reference/crm/requisites/bank-detail/crm-requisite-bank-detail-get.html

        This method returns the requisite template or bank details by its identifier.

        Args:
            bitrix_id: Identifier of the entity;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._get(bitrix_id=bitrix_id, timeout=timeout)

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
        """Get a list of entities.

        Documentation:
        https://apidocs.bitrix24.com/api-reference/crm/requisites/presets/crm-requisite-preset-list.html
        https://apidocs.bitrix24.com/api-reference/crm/requisites/bank-detail/crm-requisite-bank-detail-list.html

        The method returns a list of requisites templates or bank details based on the filter.

        Args:
            select: An array containing the list of fields to select;

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
                    field_2: value_2,
                    ...,
                    field_n: value_n,
                },

                where

                    - field_n is the name of the field by which the selection will be sorted

                    - value_n is a string value equals to 'asc' (ascending sort) or 'desc' (descending sort);

            start: This parameter is used to manage pagination;

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
    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update entity.

        Documentation:
        https://apidocs.bitrix24.com/api-reference/crm/requisites/presets/crm-requisite-preset-update.html
        https://apidocs.bitrix24.com/api-reference/crm/requisites/bank-detail/crm-requisite-bank-detail-update.html

        This method updates the requisite template or bank details.

        Args:
            bitrix_id: Identifier of the entity to be updated;

            fields: Set of template fields — an object, the values of which need to be changed;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._update(
            bitrix_id=bitrix_id,
            fields=fields,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete entity.

        Documentation:
        https://apidocs.bitrix24.com/api-reference/crm/requisites/presets/crm-requisite-preset-delete.html
        https://apidocs.bitrix24.com/api-reference/crm/requisites/bank-detail/crm-requisite-bank-detail-delete.html

        This method deletes requisite template or bank entity.

        Args:
            bitrix_id: Identifier of the entity;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._delete(bitrix_id=bitrix_id, timeout=timeout)
