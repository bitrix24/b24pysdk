from typing import Optional, Sequence, Text, Union

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import B24BoolStrict, DocumentType, JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Activity",
]


class Activity(BaseEntity):
    """Handle operations related to Bitrix24 business process custom activities.

    Documentation: https://apidocs.bitrix24.com/api-reference/bizproc/bizproc-activity/
    """

    @type_checker
    def add(
            self,
            code: Text,
            handler: Text,
            name: Union[Text, JSONDict],
            *,
            auth_user_id: Optional[int] = None,
            use_subscription: Optional[Union[bool, B24BoolStrict]] = None,
            description: Optional[Union[Text, JSONDict]] = None,
            properties: Optional[JSONDict] = None,
            return_properties: Optional[JSONDict] = None,
            document_type: Optional[Sequence[Text]] = None,
            filter: Optional[JSONDict] = None,
            use_placement: Optional[Union[bool, B24BoolStrict]] = None,
            placement_handler: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add a new custom action for use in Bitrix24 business processes.

        Documentation: https://apidocs.bitrix24.com/api-reference/bizproc/bizproc-activity/bizproc-activity-add.html

        This method registers a custom action that can be used in workflows. The operation works only
        in the application context.

        Args:
            code: Internal identifier of the action;

            handler: URL to which the action will send data via the Bitrix24 queue server;

            name: Name of the action;

            auth_user_id: Identifier of the user whose token will be passed to the application;

            use_subscription: Whether the action should wait for a response from the application;

            description: Description of the action;

            properties: Object format:
                {
                    "<PARAM_CODE>": { <parameter description object> },

                    ...,
                };
                each entry describes an action parameter;

            return_properties: Object format:
                {
                    "<PARAM_CODE>": { <parameter description object> },

                    ...,
                };
                each entry describes an additional result parameter returned by the action;

            document_type: Array of three strings defining the document type [moduleId, objectId, documentType];

            filter: Object format:
                {
                    "INCLUDE": [ <rule_1>, ..., <rule_n> ],

                    "EXCLUDE": [ <rule_1>, ..., <rule_n> ]
                };
                rules to restrict the action by document type and edition;

            use_placement: Enables opening additional action settings in the application slider;

            placement_handler: URL of the placement handler on the application side;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "CODE": code,
            "HANDLER": handler,
            "NAME": name,
        }

        if auth_user_id is not None:
            params["AUTH_USER_ID"] = auth_user_id

        if use_subscription is not None:
            params["USE_SUBSCRIPTION"] = B24BoolStrict(use_subscription).to_b24()

        if description is not None:
            params["DESCRIPTION"] = description

        if properties is not None:
            params["PROPERTIES"] = properties

        if return_properties is not None:
            params["RETURN_PROPERTIES"] = return_properties

        if document_type is not None:
            params["DOCUMENT_TYPE"] = DocumentType(document_type).to_b24()

        if filter is not None:
            params["FILTER"] = filter

        if use_placement is not None:
            params["USE_PLACEMENT"] = B24BoolStrict(use_placement).to_b24()

        if placement_handler is not None:
            params["PLACEMENT_HANDLER"] = placement_handler

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def log(
            self,
            event_token: Text,
            log_message: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Write a message to the business process log.

        Documentation: https://apidocs.bitrix24.com/api-reference/bizproc/bizproc-activity/bizproc-activity-log.html

        The method logs information into the business process log. Event logging must be enabled in the business process template.

        Args:
            event_token: Unique key required to send an event back to the workflow;

            log_message: Message to be written into the workflow log;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "EVENT_TOKEN": event_token,
            "LOG_MESSAGE": log_message,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.log,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            code: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete a custom activity previously added by the application.

        Documentation: https://apidocs.bitrix24.com/api-reference/bizproc/bizproc-activity/bizproc-activity-delete.html

        The method removes a custom activity registered by the application. Works only in the
        application context.

        Args:
            code: Symbolic identifier of the application activity to delete;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "CODE": code,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            code: Text,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update a custom business process activity added by the application.

        Documentation: https://apidocs.bitrix24.com/api-reference/bizproc/bizproc-activity/bizproc-activity-update.html

        This method updates a business process action added by the application. Works only in the application context.

        Args:
            code: Internal identifier of the activity to update;

            fields: Object format:
                {
                    "field_1": "value_1",

                    ...,

                    "field_n": "value_n",
                }

                where field_n - field of the business process action and value_n its value;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "CODE": code,
            "FIELDS": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Retrieve the list of activities installed by the application.

        Documentation: https://apidocs.bitrix24.com/api-reference/bizproc/bizproc-activity/bizproc-activity-list.html

        The API returns an array of actions defined by the application. Works only in the application context.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            timeout=timeout,
        )
