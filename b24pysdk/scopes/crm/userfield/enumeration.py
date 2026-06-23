from ....api.requests import BitrixAPIValueRequest
from ....schemas.crm.field import CRMFieldsData, CRMFieldsDict
from ....utils.functional import type_checker
from ....utils.types import Timeout
from .._base_crm import BaseCRM

__all__ = [
    "Enumeration",
]


class Enumeration(BaseCRM):
    """"""

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIValueRequest[CRMFieldsData, CRMFieldsDict]:
        """Get field descriptions for custom field type

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/user-defined-fields/crm-userfield-enumeration-fields.html

        The method returns the field descriptions for a custom field of type 'enumeration' (list).

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._fields(timeout=timeout)
