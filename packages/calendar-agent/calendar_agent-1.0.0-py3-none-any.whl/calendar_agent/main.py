import arrow
import googlemaps
import textwrap
import yaml
from agents import Agent as OpenAIAgent
from agents import function_tool
from googleapiclient.discovery import Resource
from typing import Callable


class CalendarAgent(OpenAIAgent):
    def __init__(
        self,
        calsvc: Resource,
        gmaps_api_key: str,
        model: str = 'gpt-4.1-mini',
    ) -> None:
        calendar_time_zone = calsvc.settings().get(setting='timezone').execute().get('value')

        super().__init__(
            name=self.__class__.__name__,
            model=model,
            instructions=textwrap.dedent(
                '''\
                Use the provided tools to interact with the Google Calendar API.

                # Current Time

                {current_time} ({time_zone})

                # Calendar Selection

                - if a calendar name is specified or implied, look up and use its calendar id
                - if no calendar is specified, use calendar_id='primary'.
                '''
            ).format(
                current_time=arrow.now(calendar_time_zone).format('YYYY-MM-DDTHH:mm:ssZZ'),
                time_zone=calendar_time_zone,
            ),
            output_type=str,
            tools=[
                search_events_wrapper(calsvc),
                create_event_wrapper(calsvc, gmaps_api_key),
                list_calendars_wrapper(calsvc),
            ],
        )

    @classmethod
    def simplify_event_dict(cls, orig: dict) -> dict:
        simplified = {}

        if 'summary' in orig:
            simplified['summary'] = orig['summary']
        if 'description' in orig:
            simplified['description'] = orig['description']
        if 'location' in orig:
            simplified['location'] = orig['location']
        if 'start' in orig:
            simplified['start'] = orig['start']
        if 'end' in orig:
            simplified['end'] = orig['end']
        if 'recurringEventId' in orig:
            simplified['is_recurring'] = True

        return simplified


def search_events_wrapper(cal: Resource) -> Callable:
    @function_tool
    async def search_events(
        calendar_id: str,
        time_min: str | None,
        time_max: str | None,
    ) -> str:
        """
        time_min, time_max: format should be YYYY-MM-DDTHH:mm:ssZZ
        """
        events_result = cal.events().list(
            calendarId=calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            maxResults=1001,
            singleEvents=True,
            orderBy='startTime',
        ).execute()

        events = [
            CalendarAgent.simplify_event_dict(event)
            for event in events_result.get('items', [])
        ]

        if len(events) > 1000:
            return 'Too many events. Narrow the time range and try again.'

        return yaml.dump(events)

    return search_events


def create_event_wrapper(cal: Resource, gmaps_api_key: str) -> Callable:
    @function_tool
    async def create_event(
        calendar_id: str,
        summary: str,
        description: str | None,
        location: str | None,
        start: str | None,
        end: str | None,
        is_all_day_event: bool,
    ) -> str:
        """
        start, end: format should be YYYY-MM-DDTHH:mm:ssZZ
        location: look up and append address to location

        - if start and end are both not provided, assume all day event
        - if start is provided and end is not, assume 1 hour duration
        """
        event = {}
        if summary:
            event['summary'] = summary
        if description:
            event['description'] = description
        if location:
            gmaps = googlemaps.Client(key=gmaps_api_key)
            places = gmaps.places(query=location)['results']
            if len(places) == 1:
                event['location'] = location + ' ' + places[0]['formatted_address']
            else:
                event['location'] = location
        if start:
            if is_all_day_event:
                event['start'] = {'date': arrow.get(start).format('YYYY-MM-DD')}
            else:
                event['start'] = {'dateTime': arrow.get(start).format('YYYY-MM-DDTHH:mm:ssZZ')}
        if end:
            if is_all_day_event:
                event['end'] = {'date': arrow.get(end).format('YYYY-MM-DD')}
            else:
                event['end'] = {'dateTime': arrow.get(end).format('YYYY-MM-DDTHH:mm:ssZZ')}

        saved_event = cal.events().insert(
            calendarId=calendar_id,
            body=event,
        ).execute()

        return yaml.dump(CalendarAgent.simplify_event_dict(saved_event))

    return create_event


def list_calendars_wrapper(cal: Resource) -> Callable:
    @function_tool
    async def list_calendars() -> str:
        calendars_result = cal.calendarList().list().execute()
        calendars = [
            {
                'id': calendar['id'],
                'name': calendar['summary'],
            }
            for calendar in calendars_result.get('items', [])
        ]

        return yaml.dump(calendars)

    return list_calendars
