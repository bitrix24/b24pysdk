from typing import TYPE_CHECKING, Optional

from ...._bitrix_api_request import BitrixAPIRequest
from ..base_crm import BaseCRM

if TYPE_CHECKING:
    from .userfield import Userfield


class Enumeration(BaseCRM):
    """"""

    def __init__(self, userfield: "Userfield"):
        super().__init__(scope=userfield._scope)
        self._path = self._get_path(userfield)

    def fields(
            self,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Get field descriptions for custom field type

        Documentation:

        The method returns the field descriptions for a custom field of type 'enumeration' (list).

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._fields(timeout=timeout)
