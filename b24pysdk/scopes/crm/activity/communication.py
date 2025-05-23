from typing import Optional, TYPE_CHECKING

from ...._bitrix_api_request import BitrixAPIRequest

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

    def fields(
            self,
            *,
            timeout: Optional[int] = None,
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
