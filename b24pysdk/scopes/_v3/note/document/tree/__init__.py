from functools import cached_property

from ......api.requests import BitrixAPIRequest
from ......utils.functional import type_checker
from ......utils.types import JSONDict, Timeout
from ....._base_entity import BaseEntity
from ...._field import Field

__all__ = [
    "Tree",
]


class Tree(BaseEntity):
    """Class for retrieving document tree.

    Documentation: https://apidocs.bitrix24.com/api-reference/note/document/index.html"""

    @cached_property
    def field(self) -> Field:
        """"""
        return Field(self)

    @type_checker
    def list(
            self,
            collection_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get document tree

        Documentation: https://apidocs.bitrix24.com/api-reference/note/document/note-document-tree-list.html

        The method returns the document tree of a single knowledge base.

        Args:
            collection_id: Knowledge base identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "collectionId": collection_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
