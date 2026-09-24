from functools import cached_property
from typing import Optional

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity
from ..._field import Field

__all__ = [
    "Collection",
]


class Collection(BaseEntity):
    """Methods for working with knowledge bases.

    Documentation: https://apidocs.bitrix24.com/api-reference/note/collection/index.html
    """

    @cached_property
    def field(self) -> Field:
        """"""
        return Field(self)

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create knowledge base

        Documentation: https://apidocs.bitrix24.com/api-reference/note/collection/note-collection-add.html

        The method creates a new knowledge base and returns its object.

        Args:
            fields: Object with the fields of the new knowledge base;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
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
    def archive(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Archive knowledge base

        Documentation: https://apidocs.bitrix24.com/api-reference/note/collection/note-collection-archive.html

        The method archives a knowledge base and cascades the archive to all its documents.

        Args:
            bitrix_id: Knowledge base identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.archive,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Move knowledge base to the trash

        Documentation: https://apidocs.bitrix24.com/api-reference/note/collection/note-collection-delete.html

        The method moves a knowledge base to the trash and cascades the move to all its documents.

        Args:
            bitrix_id: Knowledge base identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
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
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get knowledge base

        Documentation: https://apidocs.bitrix24.com/api-reference/note/collection/note-collection-get.html

        The method retrieves a knowledge base by identifier.

        Args:
            bitrix_id: Knowledge base identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
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
            pagination: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of knowledge bases

        Documentation: https://apidocs.bitrix24.com/api-reference/note/collection/note-collection-list.html

        The method returns a list of knowledge bases available to the user.

        Args:
            pagination: Pagination parameters;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if pagination is not MISSING:
            params["pagination"] = pagination

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Rename knowledge base

        Documentation: https://apidocs.bitrix24.com/api-reference/note/collection/note-collection-update.html

        The method changes name of an existing knowledge base.

        Args:
            bitrix_id: Knowledge base identifier;

            fields: Object with the fields that need to be changed;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
