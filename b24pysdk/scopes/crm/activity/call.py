from typing import Optional

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Call",
]


class Call(BaseEntity):
    """Class for obtaining call transcription.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/activity-base/index.html
    """

    @type_checker
    def get_transcript(
            self,
            activity_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[Optional[JSONDict]]:
        """Get call transcription

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/activity-base/crm-activity-call-get-transcript.html

        The method returns the text of a completed call transcription using a CRM activity identifier.

        Args:
            activity_id: Call type activity identifier;

            timeout: Timeout in seconds.

        Returns:
              Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "activityId": activity_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get_transcript,
            params=params,
            timeout=timeout,
        )
