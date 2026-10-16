from functools import cached_property
from typing import Literal, Optional, Sequence, Text, Union

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import B24File, JSONDict, Timeout
from ..._base_entity import BaseEntity
from .property import Property

__all__ = [
    "Item",
]


class Item(BaseEntity):
    """Class for working with data storage items.

    Documentation: https://apidocs.bitrix24.com/api-reference/entity/items/index.html
    """

    @cached_property
    def property(self) -> Property:
        """"""
        return Property(self)

    @type_checker
    def get(
            self,
            entity: Text,
            *,
            sort: Optional[JSONDict] = MISSING,
            filter: Optional[JSONDict] = MISSING,
            start: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of storage items

        Documentation: https://apidocs.bitrix24.com/api-reference/entity/items/entity-item-get.html

        The method retrieves a list of items from the application's data storage.

        Args:
            entity: Identifier of the application's data storage;

            sort: Object for sorting;

            filter: Object for filtering;

            start: Pagination parameter;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "ENTITY": entity,
        }

        if sort is not MISSING:
            params["SORT"] = sort

        if filter is not MISSING:
            params["FILTER"] = filter

        if start is not MISSING:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def add(
            self,
            entity: Text,
            name: Text,
            *,
            property_values: JSONDict = MISSING,
            section: int = MISSING,
            date_active_from: Text = MISSING,
            date_active_to: Text = MISSING,
            preview_picture: Sequence[Text] = MISSING,
            detail_picture: Sequence[Text] = MISSING,
            user_fields: JSONDict = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add storage item

        Documentation: https://apidocs.bitrix24.com/api-reference/entity/items/entity-item-add.html

        The method adds an item to the application's data storage.

        Args:
            entity: Identifier of the application's data storage;

            name: Name of the storage item;

            date_active_from: Start date of the item's section;

            date_active_to: End date of the item's activity;

            preview_picture: Preview image of the item;

            detail_picture: Detailed image of the item;

            section: Identifier of the storage section;

            property_values: Property values of the item;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "ENTITY": entity,
            "NAME": name,
        }

        if property_values is not MISSING:
            params["PROPERTY_VALUES"] = property_values

        if section is not MISSING:
            params["SECTION"] = section

        if date_active_from is not MISSING:
            params["DATE_ACTIVE_FROM"] = date_active_from

        if date_active_to is not MISSING:
            params["DATE_ACTIVE_TO"] = date_active_to

        if preview_picture is not MISSING:
            params["PREVIEW_PICTURE"] = B24File(preview_picture).to_b24()

        if detail_picture is not MISSING:
            params["DETAIL_PICTURE"] = B24File(detail_picture).to_b24()

        if user_fields is not MISSING:
            for field_code, value in user_fields.items():
                if not isinstance(field_code, str) or not field_code.startswith("UF_"):
                    raise ValueError("User field codes must start with 'UF_'")

                params[field_code] = value

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(  # noqa: C901
            self,
            entity: Text,
            bitrix_id: int,
            *,
            name: Text = MISSING,
            property_values: JSONDict = MISSING,
            section: int = MISSING,
            date_active_from: Text = MISSING,
            date_active_to: Text = MISSING,
            preview_picture: Union[Sequence[Text], Literal[False]] = MISSING,
            detail_picture: Union[Sequence[Text], Literal[False]] = MISSING,
            user_fields: JSONDict = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update a storage item

        Documentation: https://apidocs.bitrix24.com/api-reference/entity/items/entity-item-update.html

        The method updates an existing storage item.

        Args:
            entity: Identifier of the application's data storageж

            bitrix_id: Identifier of the storage item;

            name: Name of the storage item;

            property_values: Property values of the storage item;

            section: Identifier of the storage section;

            date_active_from: Start date of the item's activity;

            date_active_to: End date of the item's activity;

            preview_picture: Preview image of the item;

            detail_picture: Detailed image of the item;

            user_fields: User fields of the item;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "ENTITY": entity,
            "ID": bitrix_id,
        }

        if name is not MISSING:
            params["NAME"] = name

        if property_values is not MISSING:
            params["PROPERTY_VALUES"] = property_values

        if section is not MISSING:
            params["SECTION"] = section

        if date_active_from is not MISSING:
            params["DATE_ACTIVE_FROM"] = date_active_from

        if date_active_to is not MISSING:
            params["DATE_ACTIVE_TO"] = date_active_to

        if preview_picture is not MISSING:
            params["PREVIEW_PICTURE"] = (
                False if preview_picture is False else B24File(preview_picture).to_b24()
            )

        if detail_picture is not MISSING:
            params["DETAIL_PICTURE"] = (
                False if detail_picture is False else B24File(detail_picture).to_b24()
            )

        if user_fields is not MISSING:
            for field_code, value in user_fields.items():
                if not isinstance(field_code, str) or not field_code.startswith("UF_"):
                    raise ValueError("User field codes must start with 'UF_'")

                params[field_code] = value

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            entity: Text,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete a storage item

        Documentation: https://apidocs.bitrix24.com/api-reference/entity/items/entity-item-delete.html

        The method removes an item from the application's data storage.

        Args:
            entity: Identifier of the application's data storage;

            bitrix_id: Identifier of the storage item to be deleted;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "ENTITY": entity,
            "ID": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )
