from datetime import datetime
from typing import TYPE_CHECKING, List, Optional, Text

from ...._bitrix_api_request import BitrixAPIRequest
from ....utils.functional import type_checker
from ..base_crm import BaseCRM

if TYPE_CHECKING:
    from .activity import Activity


class Todo(BaseCRM):
    """These methods offer capabilities for managing universal activities, which are a type of activity with extended settings.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/todo/index.html
    """

    def __init__(self, activity: "Activity"):
        super().__init__(scope=activity._scope)
        self._path = self._get_path(activity)

    @type_checker
    def add(
            self,
            *,
            owner_type_id: int,
            owner_id: int,
            deadline: datetime,
            title: Optional[Text] = None,
            description: Optional[Text] = None,
            responsible_id: Optional[int] = None,
            parent_activity_id: Optional[int] = None,
            ping_offsets: Optional[List[int]] = None,
            color_id: Optional[int] = None,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Add a new universal activity.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/todo/crm-activity-todo-add.html

        The method adds a universal activity to the timeline.

        Args:
            owner_type_id: Identifier of the CRM object type to which the activity is linked;

            owner_id: Identifier of the CRM entity to which the activity is linked;

            deadline: Deadline for the activity;

            title: Title of the activity, default is an empty string;

            description: Description of the activity, default is an empty string;

            responsible_id: Identifier of the user responsible for the activity;

            parent_activity_id: Identifier of the activity in the timeline with which the created activity can be linked;

            ping_offsets: An array containing integer values in minutes that allow you to set reminder times for the activity;

            color_id: Identifier of the activity color in the timeline. There are 8 colors available, values from 1 to 7 and a default color if none is specified;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "ownerTypeId": owner_type_id,
            "ownerId": owner_id,
            "deadline": deadline,
            "title": title,
            "description": description,
            "colorId": color_id,
        }
        if ping_offsets is not None:
            params["pingOffsets"] = ping_offsets

        if responsible_id is not None:
            params["responsibleId"] = responsible_id

        if parent_activity_id is not None:
            params["parentActivityId"] = parent_activity_id

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.add),
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            bitrix_id: int,
            *,
            owner_type_id: int,
            owner_id: int,
            deadline: datetime,
            title: Optional[Text] = None,
            description: Optional[Text] = None,
            responsible_id: Optional[int] = None,
            parent_activity_id: Optional[int] = None,
            ping_offsets: Optional[List[int]] = None,
            color_id: Optional[int] = None,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Update universal activity.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/todo/crm-activity-todo-update.html

        The method updates a universal activity.

        Args:
            owner_type_id: Identifier of the CRM object type to which the activity is linked;

            owner_id: Identifier of the CRM entity to which the activity is linked;

            deadline: Deadline for the activity;

            title: Title of the activity, default is an empty string;

            description: Description of the activity, default is an empty string;

            responsible_id: Identifier of the user responsible for the activity;

            parent_activity_id: Identifier of the activity in the timeline with which the created activity can be linked;

            ping_offsets: An array containing integer values in minutes that allow you to set reminder times for the activity;

            color_id: Identifier of the activity color in the timeline. There are 8 colors available, values from 1 to 7 and a default color if none is specified;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
            "ownerTypeId": owner_type_id,
            "ownerId": owner_id,
            "deadline": deadline,
            "title": title,
            "description": description,
            "colorId": color_id,
        }

        if ping_offsets is not None:
            params["pingOffsets"] = ping_offsets

        if responsible_id is not None:
            params["responsibleId"] = responsible_id

        if parent_activity_id is not None:
            params["parentActivityId"] = parent_activity_id

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.update),
            params=params,
            timeout=timeout,
        )

    def update_color(
            self,
            bitrix_id: int,
            *,
            owner_type_id: int,
            owner_id: int,
            color_id: int,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Update the color of the universal activity.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/todo/crm-activity-todo-update-color.html

        The method updates the color of the universal activity.

        Args:
            bitrix_id: Identifier of the activity being updated;

            owner_type_id: Identifier of the CRM object type to which the activity is linked;

            owner_id: Identifier of the CRM entity to which the activity is linked;

            color_id: Identifier of the activity color in the timeline. There are 8 colors available, values from 1 to 7 and the default color if none is specified;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
            "ownerTypeId": owner_type_id,
            "ownerId": owner_id,
            "colorId": color_id,
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.update_color),
            params=params,
            timeout=timeout,
        )

    def update_deadline(
            self,
            bitrix_id: int,
            *,
            owner_type_id: int,
            owner_id: int,
            value: datetime,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Update the deadline of the universal activity.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/todo/crm-activity-todo-update-deadline.html

        The method changes the deadline of a universal activity.

        Args:
            bitrix_id: Identifier of the activity being updated;

            owner_type_id: Identifier of the CRM object type to which the activity is linked;

            owner_id: Identifier of the CRM entity to which the activity is linked;

            value: New deadline for the activity;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
            "ownerTypeId": owner_type_id,
            "ownerId": owner_id,
            "value": value,
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.update_deadline),
            params=params,
            timeout=timeout,
        )

    def update_description(
            self,
            bitrix_id: int,
            *,
            owner_type_id: int,
            owner_id: int,
            value: Text,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Update the description of the universal activity.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/todo/crm-activity-todo-update-description.html

        The method changes the description in the universal activity.

        Args:
            bitrix_id: Identifier of the activity being updated;

            owner_type_id: Identifier of the CRM object type to which the activity is linked;

            owner_id: Identifier of the CRM entity to which the activity is linked;

            value: New description of the activity;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
            "ownerTypeId": owner_type_id,
            "ownerId": owner_id,
            "value": value,
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.update_description),
            params=params,
            timeout=timeout,
        )

    def update_responsible_user(
            self,
            bitrix_id: int,
            *,
            owner_type_id: int,
            owner_id: int,
            responsible_id: int,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Update the responsible user for the universal activity.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/todo/crm-activity-todo-update-responsible-user.html

        The method updates the responsible user for the universal activity.

        Args:
            bitrix_id: Identifier of the activity being updated;

            owner_type_id: Identifier of the CRM object type to which the activity is linked;

            owner_id: Identifier of the CRM entity to which the activity is linked;

            responsible_id: Identifier of the user who will become responsible for the activity;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
            "ownerTypeId": owner_type_id,
            "ownerId": owner_id,
            "responsibleId": responsible_id,
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.update_responsible_user),
            params=params,
            timeout=timeout,
        )
