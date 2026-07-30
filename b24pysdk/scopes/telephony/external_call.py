from typing import Annotated, Iterable, Literal, Optional, Text, Union

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import classproperty, type_checker
from ...utils.types import Number, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "ExternalCall",
]


class ExternalCall(BaseEntity):
    """"""

    @classproperty
    def _name(cls) -> Text:
        return "externalCall"

    @type_checker
    def attach_record(
            self,
            call_id: Text,
            filename: Text,
            *,
            file_content: Optional[Text] = MISSING,
            record_url: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "CALL_ID": call_id,
            "FILENAME": filename,
        }

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
        """"""

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
        """"""

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
        """"""

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
        """"""

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
        """"""

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
