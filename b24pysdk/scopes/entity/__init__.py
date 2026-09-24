from functools import cached_property
from typing import Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_scope import BaseScope
from .item import Item
from .section import Section

__all__ = [
    "Entity",
]


class Entity(BaseScope):
    """Class for working with data storages.

    Documentation: https://apidocs.bitrix24.com/api-reference/entity/entities/index.html
    """

    @cached_property
    def section(self) -> Section:
        """"""
        return Section(self)

    @cached_property
    def item(self) -> Item:
        """"""
        return Item(self)

    @type_checker
    def add(
            self,
            entity: Text,
            name: Text,
            *,
            access: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create a data storage

        Documentation: https://apidocs.bitrix24.com/api-reference/entity/entities/entity-add.html

        The method creates a new data storage for the application.

        Args:
            entity: Character identifier for the storage;

            name: Name of the storage;

            access: Access permissions;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIValueRequest
        """

        params = {
            "ENTITY": entity,
            "NAME": name,
        }

        if access is not MISSING:
            params["ACCESS"] = access

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            entity: Text,
            *,
            name: Optional[Text] = MISSING,
            access: Optional[JSONDict] = MISSING,
            entity_new: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update storage parameters

        Documentation: https://apidocs.bitrix24.com/api-reference/entity/entities/entity-update.html

        The method updates the parameters of the application's data storage.

        Args:
            entity: Identifier of the application's data storage;

            name: New name for the storage;

            access: New set of access permissions;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIValueRequest
        """

        params = {
            "ENTITY": entity,
        }

        if name is not MISSING:
            params["NAME"] = name

        if access is not MISSING:
            params["ACCESS"] = access

        if entity_new is not MISSING:
            params["ENTITY_NEW"] = entity_new

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def rights(
            self,
            entity: Text,
            *,
            access: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get or modify access permissions

        Documentation: https://apidocs.bitrix24.com/api-reference/entity/entities/entity-rights.html

        The method retrieves the current set of access permissions for the application's data storage or modifies it.

        Args:
            entity: Identifier of the application's data storage;

            access: A new set of permissions;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIValueRequest
        """

        params = {
            "ENTITY": entity,
        }

        if access is not MISSING:
            params["ACCESS"] = access

        return self._make_bitrix_api_request(
            api_wrapper=self.rights,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            *,
            entity: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get storage parameters or list of storages

        Documentation: https://apidocs.bitrix24.com/api-reference/entity/entities/entity-get.html

        The method returns the parameters of the specified storage or a list of all storages of the application.

        Args:
            entity: Identifier of the application's data storage;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIValueRequest
        """

        params: JSONDict = {}

        if entity is not MISSING:
            params["ENTITY"] = entity

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            entity: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete a storage

        Documentation: https://apidocs.bitrix24.com/api-reference/entity/entities/entity-delete.html

        The method removes the application's data store.

        Args:
            entity: Identifier of the application's data storage;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIValueRequest
        """

        params = {
            "ENTITY": entity,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

