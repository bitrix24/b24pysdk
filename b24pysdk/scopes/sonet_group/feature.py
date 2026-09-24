from typing import Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Feature",
]


class Feature(BaseEntity):
    """Method for checking access permissions.

    Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/index.html
    """

    @type_checker
    def access(
            self,
            group_id: int,
            feature: Text,
            operation: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Check the access permissions of the current user

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/sonet-group-feature-access.html

        The method checks whether the current user has access to operations within the group or project functionality.

        Args:
            group_id: Identifier of the group or project;

            feature: Symbolic code of the group functionality;

            operation: Symbolic code of the operation within the functionality;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "GROUP_ID": group_id,
            "FEATURE": feature,
            "OPERATION": operation,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.access,
            params=params,
            timeout=timeout,
        )
