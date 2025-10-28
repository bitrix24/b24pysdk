from functools import cached_property

from ....bitrix_api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from .._base_crm import BaseCRM
from .enumeration import Enumeration
from .settings import Settings

__all__ = [
    "Userfield",
]


class Userfield(BaseCRM):
    """Methods for working with custom fields.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/user-defined-fields/index.html
    """

    @cached_property
    def enumeration(self) -> Enumeration:
        """"""
        return Enumeration(self)

    @cached_property
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
        return self._make_bitrix_api_request(
            api_wrapper=self.types,
            timeout=timeout,
        )
