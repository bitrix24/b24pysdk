from typing import Annotated, Iterable, Literal, Optional, Text, Union

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import classproperty, type_checker
from ...utils.types import JSONDict, Number, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "ExternalCall",
]


class ExternalCall(BaseEntity):
    """Class for working with external telephony calls.

    Documentation: https://apidocs.bitrix24.com/api-reference/telephony/index.html
    """

    @classproperty
    def _name(cls) -> Text:
        return "externalCall"

    @type_checker
    def attach_record(
            self,
            call_id: Text,
            *,
            filename: Text = MISSING,
            file_content: Text = MISSING,
            record_url: Text = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Attach a record to a completed call

        Documentation: https://apidocs.bitrix24.com/api-reference/telephony/telephony-external-call-attach-record.html

        The method attaches a record to a completed call and to the CRM activity of the call.

        Args:
            call_id: Call identifier;

            filename: The name of the record file;

            file_content: The file in Base64 encoding;

            record_url: The URL of the record on an external server;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "CALL_ID": call_id,
        }

        if filename is not MISSING:
            params["FILENAME"] = filename

        if file_content is not MISSING:
            params["FILE_CONTENT"] = file_content

        if record_url is not MISSING:
            params["RECORD_URL"] = record_url

        return self._make_bitrix_api_request(
            api_wrapper=self.attach_record,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def finish(  # noqa: C901
            self,
            call_id: Text,
            *,
            user_id: Optional[int] = MISSING,
            user_phone_inner: Optional[Text] = MISSING,
            duration: Optional[int] = MISSING,
            cost: Optional[Number] = MISSING,
            cost_currency: Optional[Text] = MISSING,
            status_code: Optional[Annotated[Text, Literal[
                "200", "304", "603", "603-S", "403", "404", "486",
                "484", "503", "480", "402", "423", "OTHER",
            ]]] = MISSING,
            failed_reason: Optional[Text] = MISSING,
            record_url: Optional[Text] = MISSING,
            vote: Optional[Literal[1, 2, 3, 4, 5]] = MISSING,
            add_to_chat: Optional[Literal[0, 1]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Finish call and log it in telephony statistics

        Documentation: https://apidocs.bitrix24.com/api-reference/telephony/telephony-external-call-finish.html

        The method ends an external call, saves it in the statistics, and logs it in the CRM activity.

        Args:
            call_id: Call identifier;

            user_id: The identifier of the user who ends the call;

            user_phone_inner: The internal number of the user;

            duration: The duration of the call in seconds;

            cost: The cost of the call;

            cost_currency: The currency of the call cost;

            status_code: The result code of the call;

            failed_reason: Text reason for the failed call;

            record_url: URL of the call recording;

            vote: Rating of the call;

            add_to_chat: Add a message about the call to the employee's chat;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if user_id is MISSING and user_phone_inner is MISSING:
            raise ValueError("Either 'user_id' or 'user_phone_inner' must be provided")

        params = {
            "CALL_ID": call_id,
        }

        if user_id is not MISSING:
            params["USER_ID"] = user_id

        if user_phone_inner is not MISSING:
            params["USER_PHONE_INNER"] = user_phone_inner

        if duration is not MISSING:
            params["DURATION"] = duration

        if cost is not MISSING:
            params["COST"] = cost

        if cost_currency is not MISSING:
            params["COST_CURRENCY"] = cost_currency

        if status_code is not MISSING:
            params["STATUS_CODE"] = status_code

        if failed_reason is not MISSING:
            params["FAILED_REASON"] = failed_reason

        if record_url is not MISSING:
            params["RECORD_URL"] = record_url

        if vote is not MISSING:
            params["VOTE"] = vote

        if add_to_chat is not MISSING:
            params["ADD_TO_CHAT"] = add_to_chat

        return self._make_bitrix_api_request(
            api_wrapper=self.finish,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def hide(
            self,
            call_id: Text,
            user_id: Union[int, Iterable[int]],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Hide call card for user

        Documentation: https://apidocs.bitrix24.com/api-reference/telephony/telephony-external-call-hide.html

        The method hides the call card for a user or a list of users.

        Args:
            call_id: Call identifier;

            user_id: Identifier or an array of user identifiers;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if user_id.__class__ is not list and not isinstance(user_id, int):
            user_id = list(user_id)

        params = {
            "CALL_ID": call_id,
            "USER_ID": user_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.hide,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def register(  # noqa: C901, PLR0912
            self,
            phone_number: Text,
            call_type: Literal[1, 2, 3, 4, 5],
            *,
            user_phone_inner: Optional[Text] = MISSING,
            user_id: Optional[int] = MISSING,
            call_start_date: Optional[Text] = MISSING,
            crm_create: Optional[Literal[0, 1]] = MISSING,
            crm_source: Optional[Text] = MISSING,
            crm_entity_type: Optional[Annotated[Text, Literal["CONTACT", "COMPANY", "LEAD"]]] = MISSING,
            crm_entity_id: Optional[int] = MISSING,
            show: Optional[Literal[0, 1]] = MISSING,
            add_to_chat: Optional[Literal[0, 1]] = MISSING,
            call_list_id: Optional[int] = MISSING,
            line_number: Optional[Text] = MISSING,
            external_call_id: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Register an external call

        Documentation: https://apidocs.bitrix24.com/api-reference/telephony/telephony-external-call-register.html

        The method registers an external call in Bitrix24.

        Args:
            phone_number: The client's phone number;

            call_type: The type of call;

            user_phone_inner: The internal number of the user;

            user_id: The identifier of the user for whom the call is registered;

            call_start_date: The date and time the call started in ISO-8601 format with timezone indication;

            crm_create: Automatic creation of a CRM object if no suitable object is found by the number;

            crm_source: The identifier of the CRM source;

            crm_entity_type: The type of CRM object to associate with the call;

            crm_entity_id: The identifier of the CRM object from;

            show: Show the call detail form after registration;

            add_to_chat: Add a message about the call to the employee's chat;

            call_list_id: The identifier of the call list to which call is linked;

            line_number: The line number of the external line;

            external_call_id: The external identifier of the call on the side of the PBX/integration;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if user_id is MISSING and user_phone_inner is MISSING:
            raise ValueError("Either 'user_id' or 'user_phone_inner' must be provided")

        params = {
            "PHONE_NUMBER": phone_number,
            "TYPE": call_type,
        }

        if user_phone_inner is not MISSING:
            params["USER_PHONE_INNER"] = user_phone_inner

        if user_id is not MISSING:
            params["USER_ID"] = user_id

        if call_start_date is not MISSING:
            params["CALL_START_DATE"] = call_start_date

        if crm_create is not MISSING:
            params["CRM_CREATE"] = crm_create

        if crm_source is not MISSING:
            params["CRM_SOURCE"] = crm_source

        if crm_entity_type is not MISSING:
            params["CRM_ENTITY_TYPE"] = crm_entity_type

        if crm_entity_id is not MISSING:
            params["CRM_ENTITY_ID"] = crm_entity_id

        if show is not MISSING:
            params["SHOW"] = show

        if add_to_chat is not MISSING:
            params["ADD_TO_CHAT"] = add_to_chat

        if call_list_id is not MISSING:
            params["CALL_LIST_ID"] = call_list_id

        if line_number is not MISSING:
            params["LINE_NUMBER"] = line_number

        if external_call_id is not MISSING:
            params["EXTERNAL_CALL_ID"] = external_call_id

        return self._make_bitrix_api_request(
            api_wrapper=self.register,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def search_crm_entities(
            self,
            phone_number: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Find a client in CRM by phone number

        Documentation: https://apidocs.bitrix24.com/api-reference/telephony/telephony-external-call-search-crm-entities.html

        The method returns CRM entities based on the client's phone number and the details of the responsible employee.

        Args:
            phone_number: The client's phone number;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "PHONE_NUMBER": phone_number,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.search_crm_entities,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def show(
            self,
            call_id: Text,
            *,
            user_id: Optional[Union[int, Iterable[int]]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Show call card to user

        Documentation: https://apidocs.bitrix24.com/api-reference/telephony/telephony-external-call-show.html

        The method displays the call card to a user or a list of users;

        Args:
            call_id: Call identifier;

            user_id: Identifier of the user or an array of user identifiers;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "CALL_ID": call_id,
        }

        if user_id is not MISSING:
            if user_id.__class__ is not list and not isinstance(user_id, int):
                user_id = list(user_id)

            params["USER_ID"] = user_id

        return self._make_bitrix_api_request(
            api_wrapper=self.show,
            params=params,
            timeout=timeout,
        )
