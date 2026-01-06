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
