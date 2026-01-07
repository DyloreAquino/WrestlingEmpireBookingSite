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

        # Exclude self from relationship choices and set initial values when editing
        if self.instance and self.instance.pk:
            self.fields['friends'].queryset = Character.objects.exclude(pk=self.instance.pk)
            self.fields['enemies'].queryset = Character.objects.exclude(pk=self.instance.pk)
            self.fields['manager'].queryset = Character.objects.exclude(pk=self.instance.pk)

            # Preselect existing relationships
            from core.models import CharacterRelationship
            friend_ids = CharacterRelationship.objects.filter(
                character=self.instance,
                relationship_type=CharacterRelationship.RelationshipType.FRIEND
            ).values_list('related_character', flat=True)
            enemy_ids = CharacterRelationship.objects.filter(
                character=self.instance,
                relationship_type=CharacterRelationship.RelationshipType.ENEMY
            ).values_list('related_character', flat=True)
            manager_rel = CharacterRelationship.objects.filter(
                character=self.instance,
                relationship_type=CharacterRelationship.RelationshipType.MANAGER
            ).first()

            self.fields['friends'].initial = Character.objects.filter(pk__in=friend_ids)
            self.fields['enemies'].initial = Character.objects.filter(pk__in=enemy_ids)
            if manager_rel:
                self.fields['manager'].initial = manager_rel.related_character

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