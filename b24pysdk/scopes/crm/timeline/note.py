from typing import TYPE_CHECKING, Optional

from ...._bitrix_api_request import BitrixAPIRequest
from ....utils.functional import type_checker
from ..base_crm import BaseCRM

if TYPE_CHECKING:
    from .timeline import Timeline


class Note(BaseCRM):
    """The methods provide capabilities for working with Notes in timeline.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/note/index.html
    """

    def __init__(self, timeline: "Timeline"):
        super().__init__(scope=timeline._scope)
        self._path = self._get_path(timeline)

    @type_checker
    def get(
            self,
            *,
            entity_type_id: int,
            entity_id: int,
            item_type: int,
            item_id: int,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Get Information about note.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/note/crm-timeline-note-get.html

        This method returns information about a note related to a timeline record.

        Args:
            entity_type_id: Identifier of the entity type to which the record belongs;

            entity_id: Identifier of the entity to which the record belongs;

            item_type: Type of the record to which the note should be applied:

                - 1 — history record
                - 2 — deal;

            item_id: Identifier of the record to which the note should be applied;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        params = {
            "entityTypeId": entity_type_id,
            "entityId": entity_id,
            "itemType": item_type,
            "itemId": item_id
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.get),
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            *,
            entity_type_id: int,
            entity_id: int,
            item_type: int,
            item_id: int,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Delete note.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/note/crm-timeline-note-delete.html

        Args:
            entity_type_id: Identifier of the entity type to which the record belongs;

            entity_id: Identifier of the entity to which the record belongs;

            item_type: Type of the record to which the note should be applied:

                - 1 — history record
                - 2 — deal;

            item_id: Identifier of the record to which the note should be applied;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        params = {
            "entityTypeId": entity_type_id,
            "entityId": entity_id,
            "itemType": item_type,
            "itemId": item_id
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.delete),
            params=params,
            timeout=timeout,
        )

    @type_checker
    def save(
            self,
            *,
            entity_type_id: int,
            entity_id: int,
            item_type: int,
            item_id: int,
            text: str,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Save note.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/note/crm-timeline-note-save.html

        Args:
            entity_type_id: Identifier of the entity type to which the record belongs;

            entity_id: Identifier of the entity to which the record belongs;

            item_type: Type of the record to which the note should be applied:

                - 1 — history record
                - 2 — deal;

            item_id: Identifier of the record to which the note should be applied;

            text: Note text;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        params = {
            "entityTypeId": entity_type_id,
            "entityId": entity_id,
            "itemType": item_type,
            "itemId": item_id,
            "text": text
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.save),
            params=params,
            timeout=timeout,
        )
