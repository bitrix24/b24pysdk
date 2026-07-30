from typing import Optional, Text, Union

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, JSONList, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Role",
]


class Role(BaseEntity):
    """Methods manage roles and permissions in the document generator.

    Documentation: https://apidocs.bitrix24.com/api-reference/document-generator/role/index.html
    """

    @type_checker
    def add(
        self,
        fields: JSONDict,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add role

        Documentation: https://apidocs.bitrix24.com/api-reference/document-generator/role/document-generator-role-add.html

        The method adds a new role.

        Args:
            fields: Role fields;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
        self,
        bitrix_id: Union[int, Text],
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete role

        Documentation: https://apidocs.bitrix24.com/api-reference/document-generator/role/document-generator-role-delete.html

        The method removes a role by its identifier.

        Args:
            bitrix_id: Role identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def fillaccesses(
        self,
        accesses: JSONList,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Bind user to roles

        Documentation: https://apidocs.bitrix24.com/api-reference/document-generator/role/document-generator-role-fill-accesses.html

        The method completely overwrites the mapping of roles to access codes.

        Args:
            accesses: An array of role bindings to access codes;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "accesses": accesses,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.fillaccesses,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
        self,
        bitrix_id: Union[int, Text],
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get role by ID

        Documentation: https://apidocs.bitrix24.com/api-reference/document-generator/role/document-generator-role-get.html

        The method returns information about the role and its access permissions.

        Args:
            bitrix_id: Role identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "id": bitrix_id,
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
        start: Optional[int] = MISSING,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of roles

        Documentation: https://apidocs.bitrix24.com/api-reference/document-generator/role/document-generator-role-list.html

        The method returns a list of roles without detailing permissions.

        Args:
            start: This parameter is used to control pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {}

        if start is not MISSING:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
        self,
        bitrix_id: Union[int, Text],
        *,
        fields: Optional[JSONDict] = MISSING,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Change role

        Documentation: https://apidocs.bitrix24.com/api-reference/document-generator/role/document-generator-role-update.html

        The method updates a role by its identifier.

        Args:
            bitrix_id: Role identifier;

            fields: Set of fields to update;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        if fields is not MISSING:
            params["fields"] = fields

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
