from typing import Dict, Iterable, Optional, Text

from ...bitrix_api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Event",
]


class Event(BaseEntity):
    """
    Handle operations related to Bitrix24 calendar events.

    Documentation: https://apidocs.bitrix24.com/api-reference/calendar/
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
        """
        Add a new event to the calendar.

        Documentation: https://apidocs.bitrix24.com/api-reference/calendar/calendar-event/calendar-event-add.html

        This method adds a new event to the calendar.

        Args:
            type: Calendar type: "user", "group", or "company_calendar";
            owner_id: ID of the calendar owner. For company calendar, use 0;
            from_date: Start date/time of the event in ISO-8601 format (e.g., "2025-06-15T18:00:00+03:00" or "2025-06-15");
            to: End date/time of the event in ISO-8601 format;
            section: Calendar section ID;
            name: Name of the event;
            attendees: List of user IDs participating in the event;
            host: ID of the meeting organizer;
            skip_time: Optional flag to treat the event as all-day: "Y" or "N";
            timezone_from: Optional timezone of the start time (e.g., "Europe/Moscow");
            timezone_to: Optional timezone of the end time;
            description: Optional description of the event;
            color: Optional background color in "#RRGGBB" format;
            text_color: Optional text color in "#RRGGBB" format;
            accessibility: Optional availability during the event: "busy", "absent", "quest", or "free";
            importance: Optional event importance: "high", "normal", or "low";
            private_event: Optional privacy flag: "Y" or "N";
            is_meeting: Optional flag indicating a meeting with participants: "Y" or "N";
            location: Optional event location;
            remind: Optional list of reminder objects;
            meeting: Optional object describing meeting settings;
            rrule: Optional recurrence rule object in iCalendar format;
            crm_fields: Optional list of CRM entity IDs with prefixes;
            timeout: Timeout for the request in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

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
        """
        Delete an event from the calendar.

        Documentation: https://apidocs.bitrix24.com/api-reference/calendar/calendar-event/calendar-event-delete.html

        This method deletes an event.

        Args:
            bitrix_id: The ID of the calendar event to delete;
            timeout: Timeout for the request in seconds.

        Returns:
            Instance of BitrixAPIRequest.
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
            from_date: Optional[Text] = None,
            to: Optional[Text] = None,
            section: Optional[Iterable[int]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve a list of calendar events.

        Documentation: https://apidocs.bitrix24.com/api-reference/calendar/calendar-event/calendar-event-get.html

        This method retrieves a list of calendar events.

        Args:
            type: Calendar type: "user", "group", or "company_calendar".
            owner_id: ID of the calendar owner (0 for company calendar).
            from_date: Start of selection period (default: 1 month before today).
            to: End of selection period (default: 3 months after today).
            section: List of section IDs to filter by.
            timeout: Timeout for the request in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "type": type,
            "ownerId": owner_id,
        }

        if from_date is not None:
            params["from"] = from_date

        if to is not None:
            params["to"] = to

        if section is not None:
            if section.__class__ is not list:
                section = list(section)

            params["section"] = section

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_by_id(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve details of a calendar event by ID.

        Documentation: https://apidocs.bitrix24.com/api-reference/calendar/calendar-event/calendar-event-get-by-id.html

        This method retrieves information about a calendar event by its identifier.

        Args:
            bitrix_id: The ID of the event to retrieve.
            timeout: Timeout for the request in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get_by_id,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_nearest(
            self,
            *,
            type: Optional[Text] = None,
            owner_id: Optional[int] = None,
            days: Optional[int] = None,
            for_current_user: Optional[bool] = None,
            max_events_count: Optional[int] = None,
            detail_url: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve the nearest upcoming calendar events.

        Documentation: https://apidocs.bitrix24.com/api-reference/calendar/calendar-event/calendar-event-get-nearest.html

        This method retrieves a list of upcoming events.

        Args:
            type: Calendar type: "user", "group", or "company_calendar".
            owner_id: ID of the calendar owner (0 for company calendar).
            days: Number of days to look ahead (default: 60).
            for_current_user: If True, returns events only for the current user (default: True).
            max_events_count: Maximum number of events to return.
            detail_url: URL to the calendar detail page.
            timeout: Timeout for the request in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """
        params = dict()

        if type is not None:
            params["type"] = type

        if owner_id is not None:
            params["ownerId"] = owner_id

        if days is not None:
            params["days"] = days

        if for_current_user is not None:
            params["forCurrentUser"] = for_current_user

        if max_events_count is not None:
            params["maxEventsCount"] = max_events_count

        if detail_url is not None:
            params["detailUrl"] = detail_url

        return self._make_bitrix_api_request(
            api_wrapper=self.get_nearest,
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
        """
        Update an existing calendar event.

        Documentation: https://apidocs.bitrix24.com/api-reference/calendar/calendar-event/calendar-event-update.html

        This method updates an existing event.

        Args:
            bitrix_id: ID of the event to update;
            type: Calendar type: "user", "group", or "company_calendar";
            owner_id: ID of the calendar owner. For company calendar, use 0;
            name: New name of the event;
            attendees: New list of user IDs participating in the event (required if is_meeting = "Y");
            host: New ID of the meeting organizer (required if is_meeting = "Y");
            from_date: Optional new start date/time of the event in ISO-8601 format;
            to: Optional new end date/time of the event in ISO-8601 format;
            section: Optional new calendar section ID;
            skip_time: Optional flag to treat the event as all-day: "Y" or "N";
            timezone_from: Optional new timezone of the start time (e.g., "Europe/Moscow");
            timezone_to: Optional new timezone of the end time;
            description: Optional new description of the event;
            color: Optional new background color in "#RRGGBB" format;
            text_color: Optional new text color in "#RRGGBB" format;
            accessibility: Optional new availability during the event: "busy", "absent", "quest", or "free";
            importance: Optional new event importance: "high", "normal", or "low";
            private_event: Optional new privacy flag: "Y" or "N";
            is_meeting: Optional new flag indicating a meeting with participants: "Y" or "N";
            location: Optional new event location;
            remind: Optional new list of reminder objects;
            meeting: Optional new object describing meeting settings;
            rrule: Optional new recurrence rule object in iCalendar format;
            crm_fields: Optional new list of CRM entity IDs with prefixes;
            recurrence_mode: Optional mode for recurring events: "this", "next", or "all";
            current_date_from: Optional date of the specific event instance being edited (required for "this" and "next" modes);
            timeout: Timeout for the request in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

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
