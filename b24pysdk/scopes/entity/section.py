from typing import Optional, Sequence, Text, Union

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import B24BoolStrict, B24File, JSONDict, Timeout
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
            sort: Optional[JSONDict] = MISSING,
            filter: Optional[JSONDict] = MISSING,
            start: Optional[int] = MISSING,
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
            description: Optional[Text] = MISSING,
            active: Optional[Union[bool, B24BoolStrict]] = MISSING,
            code: Optional[Text] = MISSING,
            sort: Optional[int] = MISSING,
            picture: Optional[Sequence[Text]] = MISSING,
            detail_picture: Optional[Sequence[Text]] = MISSING,
            section: Optional[int] = MISSING,
            timeout: Timeout = None,
            **fields,
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

        if description is not MISSING:
            params["DESCRIPTION"] = description

        if active is not MISSING:
            params["ACTIVE"] = B24BoolStrict(active).to_b24()

        if code is not MISSING:
            params["CODE"] = code

        if sort is not MISSING:
            params["SORT"] = sort

        if picture is not MISSING:
            params["PICTURE"] = B24File(picture).to_b24()

        if detail_picture is not MISSING:
            params["DETAIL_PICTURE"] = B24File(detail_picture).to_b24()

        if section is not MISSING:
            params["SECTION"] = section

        params.update(fields)

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
            name: Optional[Text] = MISSING,
            description: Optional[Text] = MISSING,
            active: Optional[Union[bool, B24BoolStrict]] = MISSING,
            code: Optional[Text] = MISSING,
            sort: Optional[int] = MISSING,
            picture: Optional[Sequence[Text]] = MISSING,
            detail_picture: Optional[Sequence[Text]] = MISSING,
            section: Optional[int] = MISSING,
            timeout: Timeout = None,
            **fields,
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

        if name is not MISSING:
            params["NAME"] = name

        if description is not MISSING:
            params["DESCRIPTION"] = description

        if active is not MISSING:
            params["ACTIVE"] = B24BoolStrict(active).to_b24()

        if code is not MISSING:
            params["CODE"] = code

        if sort is not MISSING:
            params["SORT"] = sort

        if picture is not MISSING:
            params["PICTURE"] = B24File(picture).to_b24()

        if detail_picture is not MISSING:
            params["DETAIL_PICTURE"] = B24File(detail_picture).to_b24()

        if section is not MISSING:
            params["SECTION"] = section

        params.update(fields)

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

