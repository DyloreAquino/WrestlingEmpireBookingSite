from django import forms
from booking.models import Match, Event

class AddMatchToStorylineForm(forms.Form):
    match = forms.ModelChoiceField(
        queryset=Match.objects.all(),
        label="Select Match",
        required=True
    )

class AddEventToStorylineForm(forms.Form):
    event = forms.ModelChoiceField(
        queryset=Event.objects.all(),
        label="Select Event",
        required=True
    )
