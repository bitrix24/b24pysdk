from typing import Iterable, Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from ._base_crm import BaseCRM

__all__ = [
    "Stagehistory",
]


class Stagehistory(BaseCRM):
    """The class provide a method that returns records of the stage history for one of the following elements:
        - leads,
        - deals,
        - old invoices,
        - new invoices,
        - SPAs.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/crm-stage-history-list.html
    """

    @type_checker
    def list(
            self,
            entity_type_id: int,
            *,
            select: Optional[Iterable[Text]] = MISSING,
            filter: Optional[JSONDict] = MISSING,
            order: Optional[JSONDict] = MISSING,
            start: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the stage history.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/crm-stage-history-list.html

        The method returns records of stage history for the element.

        Args:
            entity_type_id: Identifier of the object type;

            select: List of fields to retrieve;

            filter: Filtering list;

            order: Sorting list, where the key is the field and the value is

                - ASC for the ascending order,

                - DESC for the descending order;

            start: Offset for pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "entityTypeId": entity_type_id,
        }

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        if filter is not MISSING:
            params["filter"] = filter

        if order is not MISSING:
            params["order"] = order

        if start is not MISSING:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
