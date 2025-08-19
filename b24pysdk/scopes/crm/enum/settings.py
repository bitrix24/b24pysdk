from typing import TYPE_CHECKING

from ....bitrix_api.classes import BitrixAPIRequest
from ....scopes.crm.base_crm import BaseCRM
from ....utils.functional import type_checker
from ....utils.types import Timeout

if TYPE_CHECKING:
    from .enum import Enum


class Settings(BaseCRM):

    def __init__(self, enum: "Enum"):
        super().__init__(enum._scope)
        self._path = self._get_path(enum)

    @type_checker
    def mode(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get description of CRM operation modes.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/auxiliary/enum/crm-enum-settings-mode.html

        The method returns a list of CRM operation modes.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._make_bitrix_api_request(
            api_method=self.mode,
            timeout=timeout,
        )
