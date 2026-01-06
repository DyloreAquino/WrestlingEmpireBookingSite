from django import forms
from booking.models import Match, Event

class AddMatchToStorylineForm(forms.Form):
    match = forms.ModelChoiceField(queryset=Match.objects.none())

    def __init__(self, *args, available_matches=None, **kwargs):
        super().__init__(*args, **kwargs)
        if available_matches is not None:
            self.fields['match'].queryset = available_matches

class AddEventToStorylineForm(forms.Form):
    event = forms.ModelChoiceField(
        queryset=Event.objects.all(),
        label="Select Event",
        required=True
    )
