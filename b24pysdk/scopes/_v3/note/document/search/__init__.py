from functools import cached_property
from typing import Optional, Text

from ......_constants import MISSING
from ......api.requests import BitrixAPIRequest
from ......utils.functional import type_checker
from ......utils.types import JSONDict, Timeout
from ....._base_entity import BaseEntity
from ...._field import Field

__all__ = [
    "Search",
]


class Search(BaseEntity):
    """Class for retrieving documents.

    Documentation: https://apidocs.bitrix24.com/api-reference/note/document/index.html
    """

    @cached_property
    def field(self) -> Field:
        """"""
        return Field(self)

    @type_checker
    def list(
            self,
            query: Text,
            *,
            pagination: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Find documents

        Documentation: https://apidocs.bitrix24.com/api-reference/note/document/note-document-search-list.html

        The method searches for documents by heading and content.

        Args:
            query: Search query;

            pagination: Pagination object;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "query": query,
        }

        if pagination is not MISSING:
            params["pagination"] = pagination

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
