from typing import Dict, Iterable, Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Event",
]


class Event(BaseEntity):
    """Class for managing calendar events.

    Documentation: https://apidocs.bitrix24.com/api-reference/calendar/calendar-event/index.html
    """

    @type_checker
    def add(  # noqa: C901, PLR0912
            self,
            type: Text,
            owner_id: int,
            from_date: Text,
            to: Text,
            section: int,
            name: Text,
            *,
            attendees: Iterable[int] = MISSING,
            host: int = MISSING,
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
        """Add event

        Documentation: https://apidocs.bitrix24.com/api-reference/calendar/calendar-event/calendar-event-add.html

        The method adds a new event to the calendar.

        Args:
            type: Calendar type;

            owner_id: Identifier of the calendar owner;

            from_date: Start date abd time of the event;

            to: End date of the event;

            section: Calendar identifier;

            name: Event name;

            attendees: List of identifiers of event participants;

            host: Organizer identifier;

            skip_time: Pass the date value without time in the from and to parameters;

            timezone_from: Timezone of the event start date and time;

            timezone_to: Timezone of the event end date and time;

            description: Event description;

            color: Background color of the event;

            text_color: Text color of the event;

            accessibility: Accessibility during the event time;

            importance: Event importance;

            private_event: Mark indicating that the event is private;

            is_meeting: Indicator of a meeting with event participants;

            location: Venue;

            remind: Array of objects describing reminders for the event;

            meeting: Object with meeting parameters;

            rrule: Recurrence of the event in the form of an object according to the iCalendar standard;

            crm_fields: Array of CRM object identifiers to link to the event;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "type": type,
            "ownerId": owner_id,
            "from": from_date,
            "to": to,
            "section": section,
            "name": name,
        }

        if attendees is not MISSING:
            if attendees.__class__ is not list:
                attendees = list(attendees)

            params["attendees"] = attendees

        if host is not MISSING:
            params["host"] = host

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
        """Delete event

        Documentation: https://apidocs.bitrix24.com/api-reference/calendar/calendar-event/calendar-event-delete.html

        The method deletes an event.

        Args:
            bitrix_id: Identifier of the event;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            type: Text,
            owner_id: int,
            *,
            from_date: Optional[Text] = MISSING,
            to: Optional[Text] = MISSING,
            section: Optional[Iterable[int]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "type": type,
            "ownerId": owner_id,
        }

        if from_date is not MISSING:
            params["from"] = from_date

        if to is not MISSING:
            params["to"] = to

        if section is not MISSING:
            if section.__class__ is not list:
                section = list(section)

            params["section"] = section

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_nearest(
            self,
            *,
            type: Optional[Text] = MISSING,
            owner_id: Optional[int] = MISSING,
            days: Optional[int] = MISSING,
            for_current_user: Optional[bool] = MISSING,
            max_events_count: Optional[int] = MISSING,
            detail_url: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {}

        if type is not MISSING:
            params["type"] = type

        if owner_id is not MISSING:
            params["ownerId"] = owner_id

        if days is not MISSING:
            params["days"] = days

        if for_current_user is not MISSING:
            params["forCurrentUser"] = for_current_user

        if max_events_count is not MISSING:
            params["maxEventsCount"] = max_events_count

        if detail_url is not MISSING:
            params["detailUrl"] = detail_url

        return self._make_bitrix_api_request(
            api_wrapper=self.get_nearest,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def getbyid(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get event by ID

        Documentation: https://apidocs.bitrix24.com/api-reference/calendar/calendar-event/calendar-event-get-by-id.html

        The method retrieves information about a calendar event by its identifier.

        Args:
            bitrix_id: Identifier of the event;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.getbyid,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(  # noqa: C901, PLR0912, PLR0915
            self,
            bitrix_id: int,
            type: Text,
            owner_id: int,
            name: Text,
            *,
            attendees: Iterable[int] = MISSING,
            host: int = MISSING,
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
        """Update event

        Documentation: https://apidocs.bitrix24.com/api-reference/calendar/calendar-event/calendar-event-update.html

        The method updates an existing event.

        Args:
            bitrix_id: Event identifier;

            type: Calendar type;

            owner_id: Identifier of the calendar owner;

            from_date: Start date abd time of the event;

            to: End date of the event;

            section: Calendar identifier;

            name: Event name;

            attendees: List of identifiers of event participants;

            host: Organizer identifier;

            skip_time: Pass the date value without time in the from and to parameters;

            timezone_from: Timezone of the event start date and time;

            timezone_to: Timezone of the event end date and time;

            description: Event description;

            color: Background color of the event;

            text_color: Text color of the event;

            accessibility: Accessibility during the event time;

            importance: Event importance;

            private_event: Mark indicating that the event is private;

            is_meeting: Indicator of a meeting with event participants;

            location: Venue;

            remind: Array of objects describing reminders for the event;

            meeting: Object with meeting parameters;

            rrule: Recurrence of the event in the form of an object according to the iCalendar standard;

            crm_fields: Array of CRM object identifiers to link to the event;

            recurrence_mode: Parameter for partial editing of a recurring event;

            current_date_from: Date of the current event for partial editing of a recurring event;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
            "type": type,
            "ownerId": owner_id,
            "name": name,
        }

        if attendees is not MISSING:
            if attendees.__class__ is not list:
                attendees = list(attendees)

            params["attendees"] = attendees

        if host is not MISSING:
            params["host"] = host

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
