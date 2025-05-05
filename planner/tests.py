from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Event
from datetime import date, time


class EventTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.event = Event.objects.create(
            title="Test Event",
            description="This is a test event.",
            location="Test Location",
            date=date(2025, 5, 20),
            time=time(15, 30),
            organizer=self.user,
        )

    def test_event_list_requires_login(self):
        response = self.client.get(reverse("event_list"))
        self.assertRedirects(response, "/accounts/login/?next=/events/")

    def test_event_list_authenticated(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("event_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Event")

    def test_event_create(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(
            reverse("event_create"),
            {
                "title": "New Event",
                "description": "New Description",
                "location": "New Place",
                "date": "2025-06-01",
                "time": "18:00",
            },
        )
        # Check for redirection after creation
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Event.objects.count(), 2)

    def test_event_edit(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(
            reverse("event_update", args=[self.event.pk]),
            {
                "title": "Updated Title",
                "description": self.event.description,
                "location": self.event.location,
                "date": self.event.date,
                "time": self.event.time,
            },
        )
        # Check for redirection after update
        self.assertEqual(response.status_code, 302)
        self.event.refresh_from_db()
        self.assertEqual(self.event.title, "Updated Title")

    def test_event_delete(self):
        self.client.login(username="testuser", password="testpass123")
        self.client.post(reverse("event_delete", args=[self.event.pk]))
        self.assertEqual(Event.objects.count(), 0)
