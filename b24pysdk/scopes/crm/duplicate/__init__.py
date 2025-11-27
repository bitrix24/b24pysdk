from functools import cached_property
from typing import Annotated, Iterable, Literal, Optional, Text

from ....bitrix_api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from .._base_crm import BaseCRM
from .volatile_type import VolatileType

__all__ = [
    "Duplicate",
]


class Duplicate(BaseCRM):
    """Method for finding duplicates in leads, contacts or companies depending on emails or phone numbers.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/duplicates/index.html
    """

    @cached_property
    def volatile_type(self) -> VolatileType:
        """"""
        return VolatileType(self)

    @type_checker
    def find_by_comm(
            self,
            *,
            type: Annotated[Text, Literal["EMAIL", "PHONE"]],
            values: Iterable[Text],
            entity_type: Optional[Annotated[Text, Literal["LEAD", "CONTACT", "COMPANY"]]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get leads, contacts, and companies with matching data

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/duplicates/crm-duplicate-find-by-comm.html

        The method returns the identifiers of lead, contacts and companies that contain phone numbers or email addresses from a specified list.

        Args:
            type: Type of communication, where possible values:

                - EMAIL,

                - PHONE;

            values: Array of emails or phone numbers (maximum number of values - 20);

            entity_type: Type of object, where possible values are:

                - LEAD,

                - CONTACT,

                - COMPANY;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest

        """

        if values.__class__ is not list:
            values = list(values)

        params = {
            "type": type,
            "values": values,
        }

        if entity_type is not None:
            params["entity_type"] = entity_type

        return self._make_bitrix_api_request(
            api_wrapper=self.find_by_comm,
            params=params,
            timeout=timeout,
        )
