from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Comment",
]


class Comment(BaseEntity):
    """Methods for working with comments in the timeline of entities.

    Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/comment/index.html
    """

    @type_checker
    def add(
            self,
            type_id: int,
            item_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create a new comment in the timeline

        Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/comment/rpa-comment-add.html

        This method creates a new comment in the timeline of the item with the identifier itemId for the process with the identifier typeId.

        Args:
            type_id: Identifier of the process;

            item_id: Identifier of the item;

            fields: Object describing the fields of the comment;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "typeId": type_id,
            "itemId": item_id,
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
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete comment

        Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/comment/rpa-comment-delete.html

        This method deletes a comment with the identifier id that were added by the same user.

        Args:
            bitrix_id: Record identifier;

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
    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update timeline entry

        Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/comment/rpa-comment-update.html

        This method updates the timeline entry with the identifier id. It only updates the title and description fields.

        Args:
            bitrix_id: Identifier of the comment;

            fields: An object describing the fields of the comment;

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
