from abc import abstractmethod
from typing import Iterable, Optional, Text

from .....bitrix_api.requests import BitrixAPIRequest
from .....utils.types import JSONDict, Timeout
from ..._base_crm import BaseCRM

__all__ = [
    "BaseDetail",
]


class BaseDetail(BaseCRM):
    """The methods provide capabilities for managing requisite templates and bank details."""

    @abstractmethod
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get description of the entity fields.

        The method returns a formal description of the fields of the requisite template or bank details.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._fields(timeout=timeout)

    @abstractmethod
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create a new entity.

        This method creates a new requisites template or bank details.

        Args:
            fields: A set of fields - an object for adding a new entity;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._add(fields=fields, timeout=timeout)

    @abstractmethod
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Get entity by ID.

        This method returns the requisite template or bank details by its identifier.

        Args:
            bitrix_id: Identifier of the entity;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._get(bitrix_id=bitrix_id, timeout=timeout)

    @abstractmethod
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

    @abstractmethod
    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update entity.

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

    @abstractmethod
    def delete(
            self,
            bitrix_id,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete entity.

        This method deletes requisite template or bank entity.

        Args:
            bitrix_id: Identifier of the entity;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._delete(bitrix_id=bitrix_id, timeout=timeout)
