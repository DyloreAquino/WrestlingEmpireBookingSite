from django import forms
from booking.models import Match, MatchParticipant

MATCH_FINISH_CHOICES = [
    ("Pinfall", "Pinfall"),
    ("Submission", "Submission"),
    ("Countout", "Countout"),
    ("DQ", "DQ"),
    ("Unique", "Unique"),
    ("No Finish", "No Finish"),
]

class MatchSimulationForm(forms.Form):
    finish = forms.ChoiceField(choices=MATCH_FINISH_CHOICES, label="Match Finish")
    winners = forms.ModelMultipleChoiceField(
        queryset=MatchParticipant.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Winner(s)"
    )

    def __init__(self, *args, **kwargs):
        match = kwargs.pop("match")
        super().__init__(*args, **kwargs)
        # Populate winners choices with participants of this match
        self.fields["winners"].queryset = match.matchparticipant_set.all()
