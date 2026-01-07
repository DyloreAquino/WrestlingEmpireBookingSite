from django import forms
from booking.models import Match, Event

class AddMatchToStorylineForm(forms.Form):
    match = forms.ModelChoiceField(queryset=Match.objects.none())

    def __init__(self, *args, available_matches=None, **kwargs):
        super().__init__(*args, **kwargs)
        if available_matches is not None:
            self.fields['match'].queryset = available_matches

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

class AddEventToStorylineForm(forms.Form):
    event = forms.ModelChoiceField(
        queryset=Event.objects.none(),
        label="Select Event",
        required=True
    )

    def __init__(self, *args, available_events=None, **kwargs):
        super().__init__(*args, **kwargs)
        if available_events is not None:
            self.fields['event'].queryset = available_events

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
