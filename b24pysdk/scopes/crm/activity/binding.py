from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from .._base_crm import BaseCRM

__all__ = [
    "Binding",
]


class Binding(BaseCRM):
    """The methods for managing the bindings of activities to CRM entities.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/binding/index.html
    """

    @type_checker
    def add(
            self,
            activity_id: int,
            *,
            entity_type_id: int,
            entity_id: int,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add a deal binding to a CRM entity.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/binding/crm-activity-binding-add.html

        The method establishes a binding between a deal and a CRM entity. A deal can only be bound to an entity that the current user has edit access to.

        Args:
            activity_id: Integer identifier of the deal in the timeline;

            entity_type_id: Integer identifier of the CRM object type to which the deal should be bound;

            entity_id: Integer identifier of the CRM entity to which the deal should be bound;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "activityId": activity_id,
            "entityTypeId": entity_type_id,
            "entityId": entity_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def move(
            self,
            activity_id: int,
            *,
            source_entity_type_id: int,
            source_entity_id: int,
            target_entity_type_id: int,
            target_entity_id: int,
            timeout: Timeout = None,
    ):
        """Update the deal's connection with the CRM entity.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/binding/crm-activity-binding-move.html

        The method updates the connection of a deal with a CRM entity. The update is only possible if the current user has edit access to the CRM entities they are modifying.

        Args:
            activity_id: Integer identifier of the deal in the timeline;

            source_entity_type_id: Identifier of the CRM object type to which the deal is linked;

            source_entity_id: The identifier of the CRM entity to which the deal is linked;

            target_entity_type_id: Identifier of the CRM object type to which the deal should be linked;

            target_entity_id: The identifier of the CRM entity to which the deal should be linked;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "activityId": activity_id,
            "sourceEntityTypeId": source_entity_type_id,
            "sourceEntityId": source_entity_id,
            "targetEntityTypeId": target_entity_type_id,
            "targetEntityId": target_entity_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.move,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            activity_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of all bindings for the activity.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/binding/crm-activity-binding-list.html

        The method returns an array of bindings for the activity, each containing entityTypeId and entityId.
        Results include elements accessible for reading by the current user.

        Args:
            activity_id: Integer identifier of the deal in the timeline;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "activityId": activity_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            activity_id: int,
            *,
            entity_type_id: int,
            entity_id: int,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete the connection of the activity with the CRM entity.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/binding/crm-activity-binding-delete.html

        The method removes the connection of the activity with the CRM entity. The deletion of the activity binding is only possible for entities that the current user has edit access to.
        If the activity is linked to only one entity, this binding cannot be removed.

        Args:
            activity_id: Integer identifier of the deal in the timeline;

            entity_type_id: Integer identifier of the CRM object type to which the deal should be bound;

            entity_id: Integer identifier of the CRM entity to which the deal should be bound;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "activityId": activity_id,
            "entityTypeId": entity_type_id,
            "entityId": entity_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )
