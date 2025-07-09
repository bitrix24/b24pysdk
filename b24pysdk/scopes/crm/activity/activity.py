from typing import Iterable, Optional, Text

from ....bitrix_api.classes import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..base_crm import BaseCRM
from .badge import Badge
from .binding import Binding
from .communication import Communication
from .configurable import Configurable
from .layout import Layout
from .todo import Todo
from .type import Type


class Activity(BaseCRM):
    """Methods for working with system activities in the timeline.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/activity-base/index.html
    """

    @property
    def badge(self) -> Badge:
        """"""
        return Badge(self)

    @property
    def binding(self) -> Binding:
        """"""
        return Binding(self)

    @property
    def communication(self) -> Communication:
        """"""
        return Communication(self)

    @property
    def configurable(self) -> Configurable:
        """"""
        return Configurable(self)

    @property
    def layout(self) -> Layout:
        """"""
        return Layout(self)

    @property
    def todo(self) -> Todo:
        """"""
        return Todo(self)

    @property
    def type(self) -> Type:
        """"""
        return Type(self)

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get activity fields.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/activity-base/crm-activity-fields.html

        The method returns a description of the fields of the system activity.

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
        return self._add(fields, timeout=timeout)

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
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
        return self._get(bitrix_id, timeout=timeout)

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
        return self._update(
            bitrix_id,
            fields,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
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
        return self._delete(bitrix_id, timeout=timeout)
