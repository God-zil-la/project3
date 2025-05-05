from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def main():
    """Shows basic usage of the Google Calendar API.
    Creates a test event.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If no (valid) credentials, prompt the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=65091)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("calendar", "v3", credentials=creds)

    # Create a test event
    event = {
        "summary": "Test Event from Event Planner",
        "location": "Online",
        "description": "This is a test event synced from Django app.",
        "start": {
            "dateTime": "2025-05-03T15:00:00",
            "timeZone": "Europe/Stockholm",
        },
        "end": {
            "dateTime": "2025-05-03T16:00:00",
            "timeZone": "Europe/Stockholm",
        },
    }

    event = service.events().insert(calendarId="primary", body=event).execute()
    print("✅ Event created: %s" % (event.get("htmlLink")))


if __name__ == "__main__":
    main()
