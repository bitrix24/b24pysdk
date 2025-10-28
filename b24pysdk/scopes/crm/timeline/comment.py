from typing import Iterable, Optional, Text

from ....bitrix_api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from .._base_crm import BaseCRM

__all__ = [
    "Comment",
]


class Comment(BaseCRM):
    """The methods provide capabilities for working with a Comment type CRM activity in timeline.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/comments/index.html
    """

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get fields of comment.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/comments/crm-timeline-comment-fields.html

        This method retrieves fields of the Comment type deal.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._fields(timeout=timeout)

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add a new comment.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/comments/crm-timeline-comment-add.html

        This method adds a new activity of type Comment to the timeline.

        Args:
            fields: Object format:
                {
                    "ENTITY_ID": 'value',

                    "ENTITY_TYPE": 'value',

                    "COMMENT": 'value',

                    "AUTHOR_ID": 'value',

                    "FILES": [
                        [ "file name", "file content" ],

                        [ "file name", "file content" ],
                        ]
                };

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._add(fields, timeout=timeout)

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get comment by ID.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/comments/crm-timeline-comment-get.html

        This method retrieves information about a deal of type Comment.

        Args:
            bitrix_id: Integer identifier of the deal of type Comment;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._get(bitrix_id, timeout=timeout)

    @type_checker
    def list(
            self,
            *,
            select: Optional[Iterable[Text]] = None,
            filter: Optional[JSONDict] = None,
            order: Optional[JSONDict] = None,
            start: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of comments.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/comments/crm-timeline-comment-list.html

        This method retrieves a list of all comments of the specified CRM entity type.

        Args:
            select: An array containing the list of fields to select;

            filter: Object format:

                {
                    "field_1": "value_1",

                    "field_2": "value_2",

                    ...,

                    "field_n": "value_n",
                }, where ENTITY_ID and ENTITY_TYPE are required fields;

            order: Object format:

                {
                    field_1: value_1,

                    ...,
                }

                where

                - field_n is the name of the field by which the selection will be sorted

                - value_n is a string value equals to 'ASC' (ascending sort) or 'DESC' (descending sort);

            start: This parameter is used to control pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._list(
            select=select,
            filter=filter,
            order=order,
            start=start,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            entity_type_id: int,
            entity_id: int,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update comment.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/comments/crm-timeline-comment-update.html

        This method updates a Comment type deal in the timeline.

        Args:
            bitrix_id: Integer identifier of the deal of type Comment;

            fields: Object format:
                {
                    "COMMENT": "value",

                    "FILES": [
                        [ "file name", "file" ],

                        [ "file name", "file" ],
                        ]
                };

            entity_type_id: Integer identifier of the CRM entity type to which the comment is attached;

            entity_id: Integer identifier of the CRM entity to which the comment is attached;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
            "fields": fields,
            "entityTypeId": entity_type_id,
            "entityId": entity_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            entity_type_id: int,
            entity_id: int,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete comment.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/comments/crm-timeline-comment-delete.html

        This method deletes a deal of type Comment.

        Args:
            bitrix_id: Integer identifier of the deal of type Comment;

            entity_type_id: Integer identifier of the CRM entity type to which the comment is attached;

            entity_id: Integer identifier of the CRM entity to which the comment is attached;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
            "entityTypeId": entity_type_id,
            "entityId": entity_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )
