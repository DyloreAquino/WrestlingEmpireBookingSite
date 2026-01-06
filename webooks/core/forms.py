# forms.py
from django import forms
from core.models import Character, Championship

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

        for field in self.fields.values():
            field.widget.attrs.update({
                "class": (
                    "w-half rounded-md px-3 py-2 text-white "
                    "bg-gray-400 dark:bg-gray-700 "
                    "focus:outline-none focus:ring-2 focus:ring-blue-500"
                )
            })