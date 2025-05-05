from django.contrib import admin
from .models import Event, DeletedEvent

admin.site.register(Event)
admin.site.register(DeletedEvent)
