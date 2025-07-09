from typing import TYPE_CHECKING

from ....bitrix_api.classes import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..base_crm import BaseCRM

if TYPE_CHECKING:
    from .userfield import Userfield


class Enumeration(BaseCRM):
    """"""

    def __init__(self, userfield: "Userfield"):
        super().__init__(scope=userfield._scope)
        self._path = self._get_path(userfield)

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get field descriptions for custom field type

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/user-defined-fields/crm-userfield-enumeration-fields.html

        The method returns the field descriptions for a custom field of type 'enumeration' (list).

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._fields(timeout=timeout)
