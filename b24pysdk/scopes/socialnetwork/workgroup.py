from typing import Iterable, Optional, Text

from ...bitrix_api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import B24Bool, JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Workgroup",
]


class Workgroup(BaseEntity):
    """Handle operations related to Bitrix24 workgroups.

    Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/index.html
    """

    @type_checker
    def get(
            self,
            params: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve information about a specific workgroup.

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/socialnetwork-api-workgroup-get.html

        This method fetches details of the workgroup based on the provided parameters.

        Args:
            params: Parameters to be sent with the API requests;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "params": params,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            filter: Optional[JSONDict] = None,
            select: Optional[Iterable[Text]] = None,
            is_admin: Optional[bool] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Retrieve a list of workgroups based on provided filters.

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/socialnetwork-api-workgroup-list.html

        This method fetches a list of workgroups that match the filter criteria and selection fields.

        Args:
            filter: A dictionary containing filters to apply;

            select: An iterable of field names to include in the responses;

            is_admin: Boolean to specify if admin-specific data is required;

            timeout: Timeout setting for the requests in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = dict()

        if filter is not None:
            params["filter"] = filter

        if select is not None:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        if is_admin is not None:
            params["IS_ADMIN"] = B24Bool(is_admin).to_str()

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
