from django import forms
from booking.models import MatchParticipant

MATCH_FINISH_CHOICES = [
    ("Pinfall", "Pinfall"),
    ("Submission", "Submission"),
    ("Countout", "Countout"),
    ("DQ", "DQ"),
    ("Unique", "Unique"),
    ("No Finish", "No Finish"),
]

class MatchSimulationForm(forms.Form):
    finish = forms.ChoiceField(
        choices=MATCH_FINISH_CHOICES,
        label="Match Finish"
    )
    winners = forms.ModelMultipleChoiceField(
        queryset=MatchParticipant.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Winner(s)"
    )

    def __init__(self, *args, **kwargs):
        match = kwargs.pop("match")
        super().__init__(*args, **kwargs)

        # Populate winners with participants of this match
        self.fields["winners"].queryset = match.participants.all()

        # Tailwind styling
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    "class": "space-y-2"
                })
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({
                    "class": "h-5 w-5 text-blue-600"
                })
            else:
                field.widget.attrs.update({
                    "class": (
                        "w-half rounded-md px-3 py-2 text-white"
                        "bg-gray-400 dark:bg-gray-700 "
                        "focus:outline-none focus:ring-2 focus:ring-blue-500"
                    )
                })

from django import forms
from booking.models import Show, Match, MatchParticipant, Event, EventParticipant

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = [
            "title",
            "match_type",
            "stipulations",
            "championship",
            "notes",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    "class": "space-y-2"
                })
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({
                    "class": "h-5 w-5 text-blue-600"
                })
            else:
                field.widget.attrs.update({
                    "class": (
                        "w-half rounded-md px-3 py-2 text-white"
                        "bg-gray-400 dark:bg-gray-700 "
                        "focus:outline-none focus:ring-2 focus:ring-blue-500"
                    )
                })

class MatchParticipantForm(forms.ModelForm):
    class Meta:
        model = MatchParticipant
        fields = ["match", "character", "side", "won"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    "class": "space-y-2"
                })
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({
                    "class": "h-5 w-5 text-blue-600"
                })
            else:
                field.widget.attrs.update({
                    "class": (
                        "w-half rounded-md px-3 py-2 text-white"
                        "bg-gray-400 dark:bg-gray-700 "
                        "focus:outline-none focus:ring-2 focus:ring-blue-500"
                    )
                })

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["show", "title", "event_type", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    "class": "space-y-2"
                })
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({
                    "class": "h-5 w-5 text-blue-600"
                })
            else:
                field.widget.attrs.update({
                    "class": (
                        "w-half rounded-md px-3 py-2 text-white"
                        "bg-gray-400 dark:bg-gray-700 "
                        "focus:outline-none focus:ring-2 focus:ring-blue-500"
                    )
                })

class EventParticipantForm(forms.ModelForm):
    class Meta:
        model = EventParticipant
        fields = ["event", "character", "role"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    "class": "space-y-2"
                })
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({
                    "class": "h-5 w-5 text-blue-600"
                })
            else:
                field.widget.attrs.update({
                    "class": (
                        "w-half rounded-md px-3 py-2 text-white"
                        "bg-gray-400 dark:bg-gray-700 "
                        "focus:outline-none focus:ring-2 focus:ring-blue-500"
                    )
                })

class ShowForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = [
            "title",
            "show_type",
            "episode_number",
            "airing_date",
            "is_filmed",
            "is_uploaded",
            "youtube_link",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    "class": "space-y-2"
                })
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({
                    "class": "h-5 w-5 text-blue-600"
                })
            else:
                field.widget.attrs.update({
                    "class": (
                        "w-half rounded-md px-3 py-2 text-white"
                        "bg-gray-400 dark:bg-gray-700 "
                        "focus:outline-none focus:ring-2 focus:ring-blue-500"
                    )
                })
