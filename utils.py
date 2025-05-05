from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


def add_event_to_google_calendar(event):
    creds = None
    flow = InstalledAppFlow.from_client_secrets_file(
        "credentials.json", SCOPES
    )
    creds = flow.run_local_server(port=0)

    service = build("calendar", "v3", credentials=creds)

    event_data = {
        "summary": event.title,
        "location": event.location,
        "description": event.description,
        "start": {
            "dateTime": datetime.datetime.combine(
                event.date, event.time
            ).isoformat(),
            "timeZone": "America/Chicago",
        },
        "end": {
            "dateTime": (
                datetime.datetime.combine(event.date, event.time)
                + datetime.timedelta(hours=1)
            ).isoformat(),
            "timeZone": "America/Chicago",
        },
    }

    event = (
        service.events()
        .insert(calendarId="primary", body=event_data)
        .execute()
    )
    print("Event created: %s" % (event.get("htmlLink")))


try:
    flow = InstalledAppFlow.from_client_secrets_file(
        "credentials.json", SCOPES
    )
    creds = flow.run_local_server(port=0)
except Exception as e:
    print("OAuth Error:", e)
