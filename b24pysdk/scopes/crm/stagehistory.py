from typing import Iterable, Optional, Text

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
            *,
            entity_type_id: int,
            select: Optional[Iterable[Text]] = None,
            filter: Optional[JSONDict] = None,
            order: Optional[JSONDict] = None,
            start: Optional[int] = None,
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

        params = {
            "entityTypeId": entity_type_id,
        }

        if select is not None:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        if filter is not None:
            params["filter"] = filter

        if order is not None:
            params["order"] = order

        if start is not None:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
