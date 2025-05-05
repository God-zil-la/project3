from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from .models import Event, DeletedEvent
from .forms import EventForm

import datetime
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from dotenv import load_dotenv
load_dotenv()


client_id = os.environ.get("GOOGLE_CLIENT_ID")
client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")

SCOPES = ["https://www.googleapis.com/auth/calendar"]


@login_required
def sync_to_google(request, event_id):
    event = get_object_or_404(Event, pk=event_id, organizer=request.user)
    return redirect("event_detail", pk=event.id)


def google_calendar_init_view(request, event_id=None):
    try:
        print("Client ID:", client_id)
        print("Client Secret:", client_secret)

        if not client_id or not client_secret:
            return HttpResponseBadRequest("Missing Google Client credentials")

        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                }
            },
            scopes=SCOPES,
            redirect_uri="https://event-plan-10650f39d687.herokuapp.com/oauth2callback/"
        )

        # Save event ID in session if passed
        if event_id:
            request.session["sync_event_id"] = event_id

        authorization_url, state = flow.authorization_url(
            access_type="offline", include_granted_scopes="true"
        )
        request.session["google_auth_state"] = state
        return redirect(authorization_url)

    except Exception as e:
        print("OAuth Init Error:", str(e))
        return HttpResponseBadRequest(f"OAuth Init Error: {str(e)}")



@login_required
def google_calendar_redirect_view(request):
    state_in_session = request.session.get("google_auth_state")
    state_from_google = request.GET.get("state")
    if not state_in_session or state_in_session != state_from_google:
        return HttpResponseBadRequest("Invalid state (expired session or CSRF risk).")

    flow = Flow(
        client_type="web",
        client_config={
            "web": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=SCOPES,
        state=state_from_google,
        redirect_uri="https://event-plan-10650f39d687.herokuapp.com/oauth2callback/",
    )
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    credentials = flow.credentials
    service = build("calendar", "v3", credentials=credentials)

    unsynced_events = Event.objects.filter(
        organizer=request.user, google_event_id__isnull=True
    )

    for event in unsynced_events:
        start_dt = datetime.datetime.combine(event.date, event.time)
        end_dt = start_dt + datetime.timedelta(hours=1)

        event_data = {
            "summary": event.title,
            "location": event.location or "Online",
            "description": event.description or "No description.",
            "start": {"dateTime": start_dt.isoformat(), "timeZone": "Europe/Stockholm"},
            "end": {"dateTime": end_dt.isoformat(), "timeZone": "Europe/Stockholm"},
        }

        try:
            created_event = service.events().insert(
                calendarId="primary", body=event_data
            ).execute()
            event.google_event_id = created_event.get("id")
            event.save()
        except HttpError as e:
            print("Google Calendar sync error:", e)

    deleted_events = DeletedEvent.objects.filter(user=request.user)
    for deleted in deleted_events:
        try:
            service.events().delete(
                calendarId="primary", eventId=deleted.google_event_id
            ).execute()
        except HttpError as e:
            print(f"Failed to delete event {deleted.google_event_id}: {e}")
        deleted.delete()

    return redirect("event_list")


@login_required
def event_list(request):
    events = Event.objects.filter(organizer=request.user).order_by("date", "time")
    return render(request, "planner/event_list.html", {"events": events})


@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk, organizer=request.user)
    return render(request, "planner/event_detail.html", {"event": event})


@login_required
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect("event_list")
    else:
        form = EventForm()
    return render(request, "planner/event_form.html", {"form": form})


@login_required
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk, organizer=request.user)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect("event_detail", pk=event.pk)
    else:
        form = EventForm(instance=event)
    return render(request, "planner/event_form.html", {"form": form})


@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk, organizer=request.user)

    if request.method == "POST":
        if event.google_event_id:
            DeletedEvent.objects.create(
                google_event_id=event.google_event_id, user=request.user
            )
        event.delete()
        return redirect("event_list")

    return render(request, "planner/event_confirm_delete.html", {"event": event})


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")
