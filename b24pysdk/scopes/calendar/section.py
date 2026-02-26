from typing import Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Section",
]


class Section(BaseEntity):
    """Handle operations related to Bitrix24 calendar sections.

    Documentation: https://apidocs.bitrix24.com/api-reference/calendar/index.html
    """

    @type_checker
    def add(
            self,
            type: Text,
            owner_id: int,
            name: Text,
            *,
            description: Optional[Text] = None,
            color: Optional[Text] = None,
            text_color: Optional[Text] = None,
            export: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Add a new calendar section.

        Documentation: https://apidocs.bitrix24.com/api-reference/calendar/calendar-section-add.html

        This method adds a new calendar section for the user. Only the user executing
        the method can add a new calendar. Administrators can create calendars for
        other users.

        Args:
            type: The type of the calendar section;
            owner_id: The ID of the owner of the section;
            name: The name of the section;
            description: The description of the section;
            color: The color assigned to the section;
            text_color: The text color of the section;
            export: Additional parameters for exporting the section;
            timeout: The request timeout in seconds.

        Returns:
            An instance of BitrixAPIRequest for executing this request.
        """

        params = {
            "type": type,
            "ownerId": owner_id,
            "name": name,
        }

        if description is not None:
            params["description"] = description

        if color is not None:
            params["color"] = color

        if text_color is not None:
            params["text_color"] = text_color

        if export is not None:
            params["export"] = export

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            type: Text,
            owner_id: int,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Delete an existing calendar section.

        Documentation: https://apidocs.bitrix24.com/api-reference/calendar/calendar-section-delete.html

        This method deletes a calendar section identified by its Bitrix ID.

        Args:
            type: The calendar section type;
            owner_id: The ID of the section owner;
            bitrix_id: The Bitrix ID of the section to be deleted;
            timeout: The request timeout in seconds.

        Returns:
            An instance of BitrixAPIRequest for executing this request.
        """

        params = {
            "type": type,
            "ownerId": owner_id,
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            type: Text,
            owner_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve a list of calendar sections.

        Documentation: https://apidocs.bitrix24.com/api-reference/calendar/calendar-section-get.html

        This method fetches a list of calendar sections for the specified owner.

        Args:
            type: The calendar section type;
            owner_id: The ID of the section owner;
            timeout: The request timeout in seconds.

        Returns:
            An instance of BitrixAPIRequest for executing this request.
        """

        params = {
            "type": type,
            "ownerId": owner_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            type: Text,
            owner_id: int,
            bitrix_id: Text,
            *,
            name: Optional[Text] = None,
            description: Optional[Text] = None,
            color: Optional[Text] = None,
            text_color: Optional[Text] = None,
            export: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Update an existing calendar section.

        Documentation: https://apidocs.bitrix24.com/api-reference/calendar/calendar-section-update.html

        This method updates the properties of an existing calendar section.

        Args:
            type: The calendar section type;
            owner_id: The ID of the section owner;
            bitrix_id: The Bitrix ID of the section to be updated;
            name: The new name of the section;
            description: The new description of the section;
            color: The new color of the section;
            text_color: The new text color of the section;
            export: The object of the calendar export parameters;
            timeout: The request timeout in seconds.

        Returns:
            An instance of BitrixAPIRequest for executing this request.
        """

        params = {
            "type": type,
            "ownerId": owner_id,
            "id": bitrix_id,
        }

        if name is not None:
            params["name"] = name

        if description is not None:
            params["description"] = description

        if color is not None:
            params["color"] = color

        if text_color is not None:
            params["text_color"] = text_color

        if export is not None:
            params["export"] = export

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
