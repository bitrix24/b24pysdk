from ...api.requests import BitrixAPIValueRequest
from ...schemas.crm.field import CRMFieldsData, CRMFieldsDict
from ...utils.functional import type_checker
from ...utils.types import Timeout
from ._base_crm import BaseCRM

__all__ = [
    "Multifield",
]


class Multifield(BaseCRM):
    """"""

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIValueRequest[CRMFieldsData, CRMFieldsDict]:
        """Get description of multiple fields.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/auxiliary/multifield/crm-multifield-fields.html

        The method returns the description of multiple fields used to store phone numbers, email addresses, and other contact information in leads, contacts and companies.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIValueRequest
        """
        return self._fields(timeout=timeout)
