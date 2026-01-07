# forms.py
from django import forms
from core.models import Character, Championship, Group

class CharacterForm(forms.ModelForm):
    friends = forms.ModelMultipleChoiceField(
        queryset=Character.objects.all(),
        required=False
    )
    enemies = forms.ModelMultipleChoiceField(
        queryset=Character.objects.all(),
        required=False
    )
    manager = forms.ModelChoiceField(
        queryset=Character.objects.all(),
        required=False
    )
    champion = forms.ModelChoiceField(
        queryset=Championship.objects.all(),
        required=False
    )

    class Meta:
        model = Character
        fields = ["ring_name", "role", "gender", "alignment", "finisher", "active", "notes", "injured", "friends", "enemies", "manager", "champion"]

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

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["name", "group_type", "active"]

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

class ChampionshipForm(forms.ModelForm):
    class Meta:
        model = Championship
        fields = ["name", "eligibility", "is_active"]

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