from typing import Iterable, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIValueRequest, BitrixAPIValuesRequest
from ....objects.workgroup import Workgroup as WorkgroupObject
from ....schemas.socialnetwork import WorkgroupListData
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._adapters import BitrixObjectAdapter, BitrixObjectsAdapter
from ..._base_entity import BaseEntity

__all__ = [
    "Workgroup",
]


class Workgroup(BaseEntity):
    """Class for managing workgroups data.

    Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/index.html
    """

    @type_checker
    def get(
            self,
            params: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIValueRequest[JSONDict, WorkgroupObject]:
        """Retrieve data on workgroup

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/socialnetwork-api-workgroup-get.html

        The method returns information about a workgroup, project, scrum, or collaboration based on the identifier.

        Args:
            params: Request parameters for retrieving the group;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        _params = {
            "params": params,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=_params,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValueRequest,
            result_adapter=BitrixObjectAdapter(
                "workgroup",
                client=self._client,
                select=params.get("select"),
            ),
        )

    @type_checker
    def list(
            self,
            *,
            filter: JSONDict = MISSING,
            select: Iterable[Text] = MISSING,
            order: JSONDict = MISSING,
            params: JSONDict = MISSING,
            start: int = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIValuesRequest[WorkgroupListData, WorkgroupObject]:
        """Get a list of workgroups

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/socialnetwork-api-workgroup-list.html

        The method returns a list of workgroups, projects, scrums, and collaborations based on the current user's permissions.

        Args:
            filter: An object for filtering the selected records;

            select: An array of fields to be selected;

            order: An object for sorting the selected records, where the key is the field and the value is ASC or DESC;

            params: Additional request parameters;

            start: Pagination parameter;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        _params: JSONDict = {}

        if filter is not MISSING:
            _params["filter"] = filter

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)

            _params["select"] = select

        if order is not MISSING:
            _params["order"] = order

        if params is not MISSING:
            _params["params"] = params

        if start is not MISSING:
            _params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=_params,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValuesRequest,
            result_adapter=BitrixObjectsAdapter(
                "workgroup",
                client=self._client,
                wrapper="workgroups",
                select=_params.get("select"),
            ),
        )
