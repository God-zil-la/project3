import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os

# Path to the stored token (must be created after user authenticates)
TOKEN_PATH = "token.json"


def create_google_calendar_event(event):
    """
    Creates an event in the user's primary Google Calendar.
    The event parameter should be a Django model instance with
    title, description, date, and time fields.
    """

    if not os.path.exists(TOKEN_PATH):
        print("❌ Google token not found. Authenticate first.")
        return

    try:
        creds = Credentials.from_authorized_user_file(TOKEN_PATH)
        service = build("calendar", "v3", credentials=creds)

        # Combine date and time fields into a single datetime object
        start_datetime = datetime.datetime.combine(event.date, event.time)
        end_datetime = start_datetime + datetime.timedelta(hours=1)

        event_data = {
            "summary": event.title,
            "location": event.location or "No location",
            "description": event.description,
            "start": {
                "dateTime": start_datetime.isoformat(),
                "timeZone": "UTC",
            },
            "end": {
                "dateTime": end_datetime.isoformat(),
                "timeZone": "UTC",
            },
        }

        created_event = (
            service.events()
            .insert(calendarId="primary", body=event_data)
            .execute()
        )
        print("✅ Event created:", created_event.get("htmlLink"))

    except Exception as e:
        print("❌ Failed to sync event:", str(e))
