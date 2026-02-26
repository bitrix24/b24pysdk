from typing import Optional, Text, Union

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import B24BoolStrict, JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Section",
]


class Section(BaseEntity):
    """
    Handle operations related to Bitrix24 entity sections.

    Documentation: https://apidocs.bitrix24.com/api-reference/entity/sections/
    """

    @type_checker
    def get(
            self,
            entity: Text,
            *,
            sort: Optional[JSONDict] = None,
            filter: Optional[JSONDict] = None,
            start: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve a list of sections from the specified storage.

        Documentation: https://apidocs.bitrix24.com/api-reference/entity/sections/entity-section-get.html

        This method fetches sections information that belong to the specified entity storage.

        Args:
            entity: String identifier of the storage;

            sort: Object format: {
                "field": "order",
                ...
            }, where field can be ID, SECTION, NAME, CODE, ACTIVE, and more. Order can be ASC or DESC;

            filter: Object format: {
                "field": "value",
                ...
            }, applicable fields include ACTIVE, NAME, and others;

            start: Sequential number of the first section to return;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "ENTITY": entity,
        }

        if sort is not None:
            params["SORT"] = sort

        if filter is not None:
            params["FILTER"] = filter

        if start is not None:
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
            description: Optional[Text] = None,
            active: Optional[Union[bool, B24BoolStrict]] = None,
            sort: Optional[int] = None,
            picture: Optional[JSONDict] = None,
            detail_picture: Optional[JSONDict] = None,
            section: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Create a new section in the specified storage.

        Documentation: https://apidocs.bitrix24.com/api-reference/entity/sections/entity-section-add.html

        This method adds a new section to a specified storage with attributes.

        Args:
            entity: String identifier of the storage;

            name: Name of the new section;

            description: Description of the section;

            active: Boolean flag for section activity (Y|N);

            sort: Sorting order value;

            picture: JSON dictionary representing the section's picture;

            detail_picture: JSON dictionary for the section's detailed picture;

            section: Identifier of the parent section;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "ENTITY": entity,
            "NAME": name,
        }

        if description is not None:
            params["DESCRIPTION"] = description

        if active is not None:
            params["ACTIVE"] = B24BoolStrict(active).to_b24()

        if sort is not None:
            params["SORT"] = sort

        if picture is not None:
            params["PICTURE"] = picture

        if detail_picture is not None:
            params["DETAIL_PICTURE"] = detail_picture

        if section is not None:
            params["SECTION"] = section

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            entity: Text,
            bitrix_id: int,
            *,
            name: Optional[Text] = None,
            description: Optional[Text] = None,
            active: Optional[Union[bool, B24BoolStrict]] = None,
            sort: Optional[int] = None,
            picture: Optional[JSONDict] = None,
            detail_picture: Optional[JSONDict] = None,
            section: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Update the details of a section in the specified storage.

        Documentation: https://apidocs.bitrix24.com/api-reference/entity/sections/entity-section-update.html

        This method modifies attributes of an existing section in a given storage.

        Args:
            entity: String identifier of the storage;

            bitrix_id: Identifier of the section to update;

            name: New name for the section;

            description: Updated description of the section;

            active: New activity status flag (Y|N);

            sort: New sorting order value;

            picture: JSON dictionary for updating the section's picture;

            detail_picture: JSON dictionary for the section's updated detailed picture;

            section: Identifier of the new parent section;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "ENTITY": entity,
            "ID": bitrix_id,
        }

        if name is not None:
            params["NAME"] = name

        if description is not None:
            params["DESCRIPTION"] = description

        if active is not None:
            params["ACTIVE"] = B24BoolStrict(active).to_b24()

        if sort is not None:
            params["SORT"] = sort

        if picture is not None:
            params["PICTURE"] = picture

        if detail_picture is not None:
            params["DETAIL_PICTURE"] = detail_picture

        if section is not None:
            params["SECTION"] = section

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
        """
        Delete a section from the specified storage.

        Documentation: https://apidocs.bitrix24.com/api-reference/entity/sections/entity-section-delete.html

        This method removes a section from the given storage based on its ID.

        Args:
            entity: String identifier of the storage;

            bitrix_id: Identifier of the section to delete;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
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

