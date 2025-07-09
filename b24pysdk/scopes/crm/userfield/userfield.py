from ....bitrix_api.classes import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..base_crm import BaseCRM
from .enumeration import Enumeration
from .settings import Settings


class Userfield(BaseCRM):
    """Methods for working with custom fields.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/user-defined-fields/index.html
    """

    @property
    def enumeration(self) -> Enumeration:
        """"""
        return Enumeration(self)

    @property
    def settings(self) -> Settings:
        """"""
        return Settings(self)

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get description for custom fields.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/user-defined-fields/crm-userfield-fields.html

        The method returns the description of fields for custom fields.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._fields(timeout=timeout)

    @type_checker
    def types(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of user field types.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/user-defined-fields/crm-userfield-types.html

        The method returns the description of fields for user fields.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.types),
            timeout=timeout,
        )
