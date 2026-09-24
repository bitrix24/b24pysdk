from typing import Iterable, Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from .._base_crm import BaseCRM

__all__ = [
    "Trace",
]


class Trace(BaseCRM):
    """Class for managing sales intelligence in CRM.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/tracking/index.html
    """

    @type_checker
    def add(
            self,
            trace: Text,
            *,
            entities: Optional[Iterable[JSONDict]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[int]:
        """Create a sales intelligence trace

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/tracking/crm-tracking-trace-add.html

        The method creates a sales intelligence trace and returns its identifier.

        Args:
            trace: JSON string containing trace data;

            entities: Array of objects to be linked with the trace;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIValuesRequest
        """

        params: JSONDict = {
            "TRACE": trace,
        }

        if entities is not MISSING:
            if entities.__class__ is not list:
                entities = list(entities)

            params["ENTITIES"] = entities

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[None]:
        """Delete sales intelligence trace

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/tracking/crm-tracking-trace-delete.html

        The method removes a sales intelligence trace.

        Args:
            bitrix_id: Identifier of the sales intelligence trace;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIValuesRequest
        """
        return self._delete(bitrix_id, timeout=timeout)
