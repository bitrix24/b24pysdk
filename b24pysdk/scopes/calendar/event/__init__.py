from functools import cached_property
from typing import Dict, Iterable, Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity
from .get import Get

__all__ = [
    "Event",
]


class Event(BaseEntity):
    """"""

    @type_checker
    def add(  # noqa: C901, PLR0912
            self,
            type: Text,
            owner_id: int,
            from_date: Text,
            to: Text,
            section: int,
            name: Text,
            attendees: Iterable[int],
            host: int,
            *,
            skip_time: Optional[Text] = MISSING,
            timezone_from: Optional[Text] = MISSING,
            timezone_to: Optional[Text] = MISSING,
            description: Optional[Text] = MISSING,
            color: Optional[Text] = MISSING,
            text_color: Optional[Text] = MISSING,
            accessibility: Optional[Text] = MISSING,
            importance: Optional[Text] = MISSING,
            private_event: Optional[Text] = MISSING,
            is_meeting: Optional[Text] = MISSING,
            location: Optional[Text] = MISSING,
            remind: Optional[Iterable] = MISSING,
            meeting: Optional[Dict] = MISSING,
            rrule: Optional[Dict] = MISSING,
            crm_fields: Optional[Iterable[Text]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if attendees.__class__ is not list:
            attendees = list(attendees)

        params = {
            "type": type,
            "ownerId": owner_id,
            "from": from_date,
            "to": to,
            "section": section,
            "name": name,
            "attendees": attendees,
            "host": host,
        }

        if skip_time is not MISSING:
            params["skip_time"] = skip_time

        if timezone_from is not MISSING:
            params["timezone_from"] = timezone_from

        if timezone_to is not MISSING:
            params["timezone_to"] = timezone_to

        if description is not MISSING:
            params["description"] = description

        if color is not MISSING:
            params["color"] = color

        if text_color is not MISSING:
            params["text_color"] = text_color

        if accessibility is not MISSING:
            params["accessibility"] = accessibility

        if importance is not MISSING:
            params["importance"] = importance

        if private_event is not MISSING:
            params["private_event"] = private_event

        if is_meeting is not MISSING:
            params["is_meeting"] = is_meeting

        if location is not MISSING:
            params["location"] = location

        if remind is not MISSING:
            if remind.__class__ is not list:
                remind = list(remind)

            params["remind"] = remind

        if meeting is not MISSING:
            params["meeting"] = meeting

        if rrule is not MISSING:
            params["rrule"] = rrule

        if crm_fields is not MISSING:
            if crm_fields.__class__ is not list:
                crm_fields = list(crm_fields)

            params["crm_fields"] = crm_fields

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
        """"""

        params = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @cached_property
    def get(self) -> Get:
        """"""
        return Get(self)

    @type_checker
    def getbyid(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.getbyid,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(  # noqa: C901, PLR0912
            self,
            bitrix_id: int,
            type: Text,
            owner_id: int,
            name: Text,
            attendees: Iterable[int],
            host: int,
            *,
            from_date: Optional[Text] = MISSING,
            to: Optional[Text] = MISSING,
            section: Optional[int] = MISSING,
            skip_time: Optional[Text] = MISSING,
            timezone_from: Optional[Text] = MISSING,
            timezone_to: Optional[Text] = MISSING,
            description: Optional[Text] = MISSING,
            color: Optional[Text] = MISSING,
            text_color: Optional[Text] = MISSING,
            accessibility: Optional[Text] = MISSING,
            importance: Optional[Text] = MISSING,
            private_event: Optional[Text] = MISSING,
            is_meeting: Optional[Text] = MISSING,
            location: Optional[Text] = MISSING,
            remind: Optional[Iterable] = MISSING,
            meeting: Optional[Dict] = MISSING,
            rrule: Optional[Dict] = MISSING,
            crm_fields: Optional[Iterable[Text]] = MISSING,
            recurrence_mode: Optional[Text] = MISSING,
            current_date_from: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if attendees.__class__ is not list:
            attendees = list(attendees)

        params = {
            "id": bitrix_id,
            "type": type,
            "ownerId": owner_id,
            "name": name,
            "attendees": attendees,
            "host": host,
        }

        if from_date is not MISSING:
            params["from"] = from_date

        if to is not MISSING:
            params["to"] = to

        if section is not MISSING:
            params["section"] = section

        if skip_time is not MISSING:
            params["skip_time"] = skip_time

        if timezone_from is not MISSING:
            params["timezone_from"] = timezone_from

        if timezone_to is not MISSING:
            params["timezone_to"] = timezone_to

        if description is not MISSING:
            params["description"] = description

        if color is not MISSING:
            params["color"] = color

        if text_color is not MISSING:
            params["text_color"] = text_color

        if accessibility is not MISSING:
            params["accessibility"] = accessibility

        if importance is not MISSING:
            params["importance"] = importance

        if private_event is not MISSING:
            params["private_event"] = private_event

        if is_meeting is not MISSING:
            params["is_meeting"] = is_meeting

        if location is not MISSING:
            params["location"] = location

        if remind is not MISSING:
            if remind.__class__ is not list:
                remind = list(remind)

            params["remind"] = remind

        if meeting is not MISSING:
            params["meeting"] = meeting

        if rrule is not MISSING:
            params["rrule"] = rrule

        if crm_fields is not MISSING:
            if crm_fields.__class__ is not list:
                crm_fields = list(crm_fields)

            params["crm_fields"] = crm_fields

        if recurrence_mode is not MISSING:
            params["recurrence_mode"] = recurrence_mode

        if current_date_from is not MISSING:
            params["current_date_from"] = current_date_from

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
