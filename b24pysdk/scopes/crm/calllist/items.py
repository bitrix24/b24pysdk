from typing import TYPE_CHECKING, Optional

from ....bitrix_api.classes import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..base_crm import BaseCRM

if TYPE_CHECKING:
    from .calllist import Calllist


class Items(BaseCRM):
    """The class provides method that returns the list of participants for the call.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/call-list/index.html
    """

    def __init__(self, calllist: "Calllist"):
        super().__init__(calllist._scope)
        self._path = self._get_path(calllist)

    @type_checker
    def get(
            self,
            list_id: int,
            filter: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of participants for the call.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/call-list/crm-calllist-items-get.html

        The method returns a list of participants, contacts, or companies, along with the call status.

        Args:
            list_id: Identifier of the call;

            filter: Filter by the call status of the item;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "LIST_ID": list_id,
        }

        if filter is not None:
            params["FILTER"] = filter

        return self._make_bitrix_api_request(
            api_method=self.get,
            params=params,
            timeout=timeout,
        )
