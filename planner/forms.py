from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "location", "date", "time"]
        widgets = {
            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "placeholder": "yyyy-mm-dd",  # <-- This line ensures the placeholder
                }
            ),
            "time": forms.TimeInput(attrs={"type": "time"}),
        }
