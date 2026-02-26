from typing import Optional, Sequence, Text, Union

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import B24BoolStrict, DocumentType, JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Robot",
]


class Robot(BaseEntity):
    """Handle operations related to Bitrix24 Bizproc robots.

    Documentation: https://apidocs.bitrix24.com/api-reference/bizproc/bizproc-robot/
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
        """Register a new Bizproc robot.

        Documentation: https://apidocs.bitrix24.com/api-reference/bizproc/bizproc-robot/bizproc-robot-add.html

        The method registers a new robot. Works only in the application context.

        Args:
            code: Internal robot identifier (unique within the application);

            handler: URL to which the robot will send data via the Bitrix24 queue server;

            name: Robot name;

            auth_user_id: Identifier of the user whose token will be passed to the application;

            use_subscription: Whether the robot should wait for a response from the application;

            description: Robot description;

            properties: An object with robot parameters;

            return_properties: An object with additional results from the robot;

            document_type: Array of three strings that defines the document type and resolves data types for PROPERTIES and RETURN_PROPERTIES;

            filter: Object format:
                {
                    'INCLUDE': [ <rule_or_document_type>, ... ],

                    'EXCLUDE': [ <rule_or_document_type>, ... ],

                }

                where
                - rule_or_document_type can be a string or an array representing full or partial document type;

                - to limit by edition use: 'b24' for cloud, 'box' for self-hosted;

            use_placement: Enables opening additional robot settings in the application slider;

            placement_handler: URL of the placement handler on the application side.

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
    def update(
            self,
            code: Text,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update fields of a robot registered by the application.

        Documentation: https://apidocs.bitrix24.com/api-reference/bizproc/bizproc-robot/bizproc-robot-update.html

        This method updates the fields of a robot registered by the application. Works only in the application context.

        Args:
            code: Internal robot identifier;

            fields: Object format:
                {
                    "field_1": "value_1",

                    ...,

                    "field_n": "value_n",
                }

                where field_n - field of the robot and value_n its value;

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
        """Retrieve a list of robots registered by the application.

        Documentation: https://apidocs.bitrix24.com/api-reference/bizproc/bizproc-robot/bizproc-robot-list.html

        The method returns a list of robots registered by the application. Works only in the application context.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            code: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete a robot registered by the application.

        Documentation: https://apidocs.bitrix24.com/api-reference/bizproc/bizproc-robot/bizproc-robot-delete.html

        This method removes a robot registered by the application. Works only in the application context.

        Args:
            code: Symbolic identifier of the application's robot;

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
