from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    synced = models.BooleanField(default=False)
    google_event_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title


class DeletedEvent(models.Model):
    google_event_id = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Deleted Google Event: {self.google_event_id}"
