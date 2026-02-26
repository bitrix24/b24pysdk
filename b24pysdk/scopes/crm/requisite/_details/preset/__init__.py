from functools import cached_property
from typing import Iterable, Optional, Text

from ......api.requests import BitrixAPIRequest
from ......utils.functional import type_checker
from ......utils.types import JSONDict, Timeout
from ..base_detail import BaseDetail
from .field import Field

__all__ = [
    "Preset",
]


class Preset(BaseDetail):
    """The class provide methods for working with requisite templates.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/requisites/presets/index.html
    """

    @cached_property
    def field(self) -> Field:
        """"""
        return Field(self)

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get description of the entity fields.

        Documentation:
        https://apidocs.bitrix24.com/api-reference/crm/requisites/presets/crm-requisite-preset-fields.html

        The method returns a formal description of the fields of the requisite template or bank details.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return super().fields(timeout=timeout)

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

        This method creates a new requisites template or bank details.

        Args:
            fields: A set of fields - an object for adding a new entity;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return super().add(fields=fields, timeout=timeout)

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

        This method returns the requisite template or bank details by its identifier.

        Args:
            bitrix_id: Identifier of the entity;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return super().get(bitrix_id=bitrix_id, timeout=timeout)

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
        return super().list(
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

        This method updates the requisite template or bank details.

        Args:
            bitrix_id: Identifier of the entity to be updated;

            fields: Set of template fields — an object, the values of which need to be changed;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return super().update(
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

        This method deletes requisite template or bank entity.

        Args:
            bitrix_id: Identifier of the entity;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return super().delete(bitrix_id=bitrix_id, timeout=timeout)

    @type_checker
    def countries(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of countries for the template.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/requisites/presets/crm-requisite-preset-countries.html

        THe method returns a possible list of countries for requisite template.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.countries,
            timeout=timeout,
        )
