from typing import TYPE_CHECKING

from ....bitrix_api.classes import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..base_crm import BaseCRM

if TYPE_CHECKING:
    from .activity import Activity


class Communication(BaseCRM):
    """Method for working with system activities in the timeline

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/activity-base/index.html
    """

    def __init__(self, activity: "Activity"):
        super().__init__(scope=activity._scope)
        self._path = self._get_path(activity)

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get description of communication.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/activity-base/crm-activity-communication-fields.html

        The method returns the description of communication for an activity.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._fields(timeout=timeout)
