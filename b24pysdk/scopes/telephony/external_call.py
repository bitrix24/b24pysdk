from typing import Annotated, Iterable, Literal, Optional, Text, Union

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
            file_content: Optional[Text] = None,
            record_url: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "CALL_ID": call_id,
            "FILENAME": filename,
        }

        if file_content is not None:
            params["FILE_CONTENT"] = file_content

        if record_url is not None:
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
            user_id: Optional[int] = None,
            user_phone_inner: Optional[Text] = None,
            duration: Optional[int] = None,
            cost: Optional[Number] = None,
            cost_currency: Optional[Text] = None,
            status_code: Optional[Annotated[Text, Literal[
                "200", "304", "603", "603-S", "403", "404", "486",
                "484", "503", "480", "402", "423", "OTHER",
            ]]] = None,
            failed_reason: Optional[Text] = None,
            record_url: Optional[Text] = None,
            vote: Optional[Literal[1, 2, 3, 4, 5]] = None,
            add_to_chat: Optional[Literal[0, 1]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if user_id is None and user_phone_inner is None:
            raise ValueError("Either 'user_id' or 'user_phone_inner' must be provided")

        params = {
            "CALL_ID": call_id,
        }

        if user_id is not None:
            params["USER_ID"] = user_id

        if user_phone_inner is not None:
            params["USER_PHONE_INNER"] = user_phone_inner

        if duration is not None:
            params["DURATION"] = duration

        if cost is not None:
            params["COST"] = cost

        if cost_currency is not None:
            params["COST_CURRENCY"] = cost_currency

        if status_code is not None:
            params["STATUS_CODE"] = status_code

        if failed_reason is not None:
            params["FAILED_REASON"] = failed_reason

        if record_url is not None:
            params["RECORD_URL"] = record_url

        if vote is not None:
            params["VOTE"] = vote

        if add_to_chat is not None:
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
            user_phone_inner: Optional[Text] = None,
            user_id: Optional[int] = None,
            call_start_date: Optional[Text] = None,
            crm_create: Optional[Literal[0, 1]] = None,
            crm_source: Optional[Text] = None,
            crm_entity_type: Optional[Annotated[Text, Literal["CONTACT", "COMPANY", "LEAD"]]] = None,
            crm_entity_id: Optional[int] = None,
            show: Optional[Literal[0, 1]] = None,
            add_to_chat: Optional[Literal[0, 1]] = None,
            call_list_id: Optional[int] = None,
            line_number: Optional[Text] = None,
            external_call_id: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if user_id is None and user_phone_inner is None:
            raise ValueError("Either 'user_id' or 'user_phone_inner' must be provided")

        params = {
            "PHONE_NUMBER": phone_number,
            "TYPE": call_type,
        }

        if user_phone_inner is not None:
            params["USER_PHONE_INNER"] = user_phone_inner

        if user_id is not None:
            params["USER_ID"] = user_id

        if call_start_date is not None:
            params["CALL_START_DATE"] = call_start_date

        if crm_create is not None:
            params["CRM_CREATE"] = crm_create

        if crm_source is not None:
            params["CRM_SOURCE"] = crm_source

        if crm_entity_type is not None:
            params["CRM_ENTITY_TYPE"] = crm_entity_type

        if crm_entity_id is not None:
            params["CRM_ENTITY_ID"] = crm_entity_id

        if show is not None:
            params["SHOW"] = show

        if add_to_chat is not None:
            params["ADD_TO_CHAT"] = add_to_chat

        if call_list_id is not None:
            params["CALL_LIST_ID"] = call_list_id

        if line_number is not None:
            params["LINE_NUMBER"] = line_number

        if external_call_id is not None:
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
            user_id: Optional[Union[int, Iterable[int]]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "CALL_ID": call_id,
        }

        if user_id is not None:
            if user_id.__class__ is not list and not isinstance(user_id, int):
                user_id = list(user_id)

            params["USER_ID"] = user_id

        return self._make_bitrix_api_request(
            api_wrapper=self.show,
            params=params,
            timeout=timeout,
        )
