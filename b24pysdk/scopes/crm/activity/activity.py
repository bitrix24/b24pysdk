from typing import Iterable, Optional, Text

from ...._bitrix_api_request import BitrixAPIRequest
from ....utils.types import JSONDict

from ..base_crm import BaseCRM

from .binding import Binding
from .communication import Communication
from .todo import Todo


class Activity(BaseCRM):
    """Methods for working with system activities in the timeline.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/activity-base/index.html
    """

    def fields(
            self,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Get activity fields.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/activity-base/crm-activity-fields.html

        The method returns a description of the fields of the system activity.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return super().fields(timeout=timeout)

    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Create a new activity

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/activity-base/crm-activity-add.html

        The method creates a new system activity.

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
        return super().fields(fields, timeout=timeout)

    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Get activity by ID.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/activity-base/crm-activity-get.html

        The method returns information about the activity by its ID.

        Args:
            bitrix_id: Identifier of the activity;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return super().get(bitrix_id, timeout=timeout)

    def list(
            self,
            *,
            select: Optional[Iterable[Text]] = None,
            filter: Optional[JSONDict] = None,
            order: Optional[JSONDict] = None,
            start: Optional[int] = None,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Get a list of activities.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/activity-base/crm-activity-list.html

        The method returns a list of activities based on the filter, considering the permissions of the current user.

        Args:
            select: List of fields that should be populated in the selected elements;

            filter: Object in the format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
                }

            order: Object format:

                {
                    field_1: value_1,

                    ...,
                }

                where

                - field_n is the name of the field by which the selection will be sorted

                - value_n is a string value equals to 'ASC' (ascending sort) or 'DESC' (descending sort);

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

    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Update activity.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/activity-base/crm-activity-update.html

        The method updates an existing activity.

        Args:
            bitrix_id: Identifier of the activity to be changed;

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
        return super().update(
            bitrix_id,
            fields,
            timeout=timeout,
        )

    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Delete activity.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/activity-base/crm-activity-delete.html

        The method removes an activity of any type.

        Args:
            bitrix_id: Identifier of the activity;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return super().update(bitrix_id, timeout=timeout)

    @property
    def communication(self) -> Communication:
        """"""
        return Communication(self)

    @property
    def binding(self) -> Binding:
        """"""
        return Binding(self)

    @property
    def todo(self) -> Todo:
        """"""
        return Todo(self)
