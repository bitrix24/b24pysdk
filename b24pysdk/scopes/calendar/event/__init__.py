from functools import cached_property
from typing import Dict, Iterable, Optional, Text

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
            skip_time: Optional[Text] = None,
            timezone_from: Optional[Text] = None,
            timezone_to: Optional[Text] = None,
            description: Optional[Text] = None,
            color: Optional[Text] = None,
            text_color: Optional[Text] = None,
            accessibility: Optional[Text] = None,
            importance: Optional[Text] = None,
            private_event: Optional[Text] = None,
            is_meeting: Optional[Text] = None,
            location: Optional[Text] = None,
            remind: Optional[Iterable] = None,
            meeting: Optional[Dict] = None,
            rrule: Optional[Dict] = None,
            crm_fields: Optional[Iterable[Text]] = None,
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

        if skip_time is not None:
            params["skip_time"] = skip_time

        if timezone_from is not None:
            params["timezone_from"] = timezone_from

        if timezone_to is not None:
            params["timezone_to"] = timezone_to

        if description is not None:
            params["description"] = description

        if color is not None:
            params["color"] = color

        if text_color is not None:
            params["text_color"] = text_color

        if accessibility is not None:
            params["accessibility"] = accessibility

        if importance is not None:
            params["importance"] = importance

        if private_event is not None:
            params["private_event"] = private_event

        if is_meeting is not None:
            params["is_meeting"] = is_meeting

        if location is not None:
            params["location"] = location

        if remind is not None:
            if remind.__class__ is not list:
                remind = list(remind)

            params["remind"] = remind

        if meeting is not None:
            params["meeting"] = meeting

        if rrule is not None:
            params["rrule"] = rrule

        if crm_fields is not None:
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
    def get_by_id(
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
            api_wrapper=self.get_by_id,
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
            from_date: Optional[Text] = None,
            to: Optional[Text] = None,
            section: Optional[int] = None,
            skip_time: Optional[Text] = None,
            timezone_from: Optional[Text] = None,
            timezone_to: Optional[Text] = None,
            description: Optional[Text] = None,
            color: Optional[Text] = None,
            text_color: Optional[Text] = None,
            accessibility: Optional[Text] = None,
            importance: Optional[Text] = None,
            private_event: Optional[Text] = None,
            is_meeting: Optional[Text] = None,
            location: Optional[Text] = None,
            remind: Optional[Iterable] = None,
            meeting: Optional[Dict] = None,
            rrule: Optional[Dict] = None,
            crm_fields: Optional[Iterable[Text]] = None,
            recurrence_mode: Optional[Text] = None,
            current_date_from: Optional[Text] = None,
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

        if from_date is not None:
            params["from"] = from_date

        if to is not None:
            params["to"] = to

        if section is not None:
            params["section"] = section

        if skip_time is not None:
            params["skip_time"] = skip_time

        if timezone_from is not None:
            params["timezone_from"] = timezone_from

        if timezone_to is not None:
            params["timezone_to"] = timezone_to

        if description is not None:
            params["description"] = description

        if color is not None:
            params["color"] = color

        if text_color is not None:
            params["text_color"] = text_color

        if accessibility is not None:
            params["accessibility"] = accessibility

        if importance is not None:
            params["importance"] = importance

        if private_event is not None:
            params["private_event"] = private_event

        if is_meeting is not None:
            params["is_meeting"] = is_meeting

        if location is not None:
            params["location"] = location

        if remind is not None:
            if remind.__class__ is not list:
                remind = list(remind)

            params["remind"] = remind

        if meeting is not None:
            params["meeting"] = meeting

        if rrule is not None:
            params["rrule"] = rrule

        if crm_fields is not None:
            if crm_fields.__class__ is not list:
                crm_fields = list(crm_fields)

            params["crm_fields"] = crm_fields

        if recurrence_mode is not None:
            params["recurrence_mode"] = recurrence_mode

        if current_date_from is not None:
            params["current_date_from"] = current_date_from

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
