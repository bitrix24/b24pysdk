from typing import Iterable, Optional, Text, Union

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import Number, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Externalcall",
]


class Externalcall(BaseEntity):
    """"""

    @type_checker
    def finish(
            self,
            call_id: Text,
            user_id: int,
            duration: int,
            *,
            cost: Optional[Number] = None,
            cost_currency: Optional[Text] = None,
            status_code: Optional[Text] = None,
            failed_reason: Optional[Text] = None,
            record_url: Optional[Text] = None,
            vote: Optional[int] = None,
            add_to_chat: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "CALL_ID": call_id,
            "USER_ID": user_id,
            "DURATION": duration,
        }

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
    def register(
            self,
            user_phone_inner: Text,
            user_id: int,
            phone_number: Text,
            call_type: int,
            *,
            call_start_date: Optional[Text] = None,
            crm_create: Optional[int] = None,
            crm_source: Optional[Text] = None,
            crm_entity_type: Optional[Text] = None,
            crm_entity_id: Optional[int] = None,
            show: Optional[int] = None,
            call_list_id: Optional[int] = None,
            line_number: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "USER_PHONE_INNER": user_phone_inner,
            "USER_ID": user_id,
            "PHONE_NUMBER": phone_number,
            "TYPE": call_type,
        }

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

        if call_list_id is not None:
            params["CALL_LIST_ID"] = call_list_id

        if line_number is not None:
            params["LINE_NUMBER"] = line_number

        return self._make_bitrix_api_request(
            api_wrapper=self.register,
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
