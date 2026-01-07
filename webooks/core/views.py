from django.shortcuts import render

from django.views.generic import ListView, DetailView, CreateView, UpdateView
from core.models import Character, Group, Championship
from core.forms import CharacterForm, GroupForm, ChampionshipForm
from booking.models import MatchParticipant, EventParticipant
from django.urls import reverse_lazy

class CharacterListView(ListView):
    model = Character
    template_name = "core/character_list.html"
    context_object_name = "characters"
    paginate_by = 20  # optional pagination

    def get_queryset(self):
        qs = super().get_queryset()

        # Filters from GET params
        role = self.request.GET.get("role")
        alignment = self.request.GET.get("alignment")
        active = self.request.GET.get("active")

        if role:
            qs = qs.filter(role=role)
        if alignment:
            qs = qs.filter(alignment=alignment)
        if active:
            if active.lower() == "true":
                qs = qs.filter(active=True)
            elif active.lower() == "false":
                qs = qs.filter(active=False)

        return qs.order_by("ring_name")

class CharacterDetailView(DetailView):
    model = Character
    template_name = "core/character_detail.html"
    context_object_name = "character"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        character = self.object

        # Matches participated in
        context["matches"] = MatchParticipant.objects.filter(character=character)

        # Events participated in
        context["events"] = EventParticipant.objects.filter(character=character)

        # Win-Loss stats
        wins = MatchParticipant.objects.filter(character=character, won=True).count()
        total_matches = MatchParticipant.objects.filter(character=character).count()
        context["win_loss_ratio"] = f"{wins} / {total_matches}" if total_matches else "0 / 0"

        # Storyline points (optional) - StorylinePoint uses GenericForeignKey, so query directly
        from storylines.models import StorylinePoint
        from django.contrib.contenttypes.models import ContentType
        character_ct = ContentType.objects.get_for_model(Character)
        context["storyline_points"] = StorylinePoint.objects.filter(
            content_type=character_ct,
            object_id=character.id
        )

        return context

class CharacterCreateView(CreateView):
    model = Character
    form_class = CharacterForm
    template_name = "core/character_form.html"
    success_url = reverse_lazy("character-list")

    def form_valid(self, form):
        response = super().form_valid(form)
        # Sync relationships after saving
        from core.models import CharacterRelationship
        character = self.object

        # Clear any existing relationships of these types (should be none for new)
        CharacterRelationship.objects.filter(
            character=character,
            relationship_type__in=[
                CharacterRelationship.RelationshipType.FRIEND,
                CharacterRelationship.RelationshipType.ENEMY,
                CharacterRelationship.RelationshipType.MANAGER,
            ],
        ).delete()

        # Create friend relationships
        for f in form.cleaned_data.get('friends') or []:
            if f != character:
                CharacterRelationship.objects.create(
                    character=character,
                    related_character=f,
                    relationship_type=CharacterRelationship.RelationshipType.FRIEND
                )

        # Create enemy relationships
        for e in form.cleaned_data.get('enemies') or []:
            if e != character:
                CharacterRelationship.objects.create(
                    character=character,
                    related_character=e,
                    relationship_type=CharacterRelationship.RelationshipType.ENEMY
                )

        # Manager (single)
        manager = form.cleaned_data.get('manager')
        if manager and manager != character:
            CharacterRelationship.objects.create(
                character=character,
                related_character=manager,
                relationship_type=CharacterRelationship.RelationshipType.MANAGER
            )

        return response

class CharacterUpdateView(UpdateView):
    model = Character
    form_class = CharacterForm
    template_name = "core/character_form.html"
    success_url = reverse_lazy("character-list")

    def form_valid(self, form):
        response = super().form_valid(form)
        from core.models import CharacterRelationship
        character = self.object

        # Clear existing relationship entries for this character for these types
        CharacterRelationship.objects.filter(
            character=character,
            relationship_type__in=[
                CharacterRelationship.RelationshipType.FRIEND,
                CharacterRelationship.RelationshipType.ENEMY,
                CharacterRelationship.RelationshipType.MANAGER,
            ],
        ).delete()

        # Recreate based on form data
        for f in form.cleaned_data.get('friends') or []:
            if f != character:
                CharacterRelationship.objects.create(
                    character=character,
                    related_character=f,
                    relationship_type=CharacterRelationship.RelationshipType.FRIEND
                )

        for e in form.cleaned_data.get('enemies') or []:
            if e != character:
                CharacterRelationship.objects.create(
                    character=character,
                    related_character=e,
                    relationship_type=CharacterRelationship.RelationshipType.ENEMY
                )

        manager = form.cleaned_data.get('manager')
        if manager and manager != character:
            CharacterRelationship.objects.create(
                character=character,
                related_character=manager,
                relationship_type=CharacterRelationship.RelationshipType.MANAGER
            )

        return response


class GroupListView(ListView):
    model = Group
    template_name = "core/group_list.html"
    context_object_name = "groups"
    paginate_by = 20

class GroupDetailView(DetailView):
    model = Group
    template_name = "core/group_detail.html"
    context_object_name = "group"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = self.object
        context["members"] = group.members.all()
        return context

class GroupCreateView(CreateView):
    model = Group
    form_class = GroupForm
    template_name = "core/group_form.html"
    success_url = reverse_lazy("group-list")

class GroupUpdateView(UpdateView):
    model = Group
    form_class = GroupForm
    template_name = "core/group_form.html"
    success_url = reverse_lazy("group-list")

class ChampionshipListView(ListView):
    model = Championship
    template_name = "core/championship_list.html"
    context_object_name = "championships"

class ChampionshipDetailView(DetailView):
    model = Championship
    template_name = "core/championship_detail.html"
    context_object_name = "championship"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Current champion(s)
        context["current_reigns"] = self.object.reigns.filter(end_date__isnull=True)
        # Full title history
        context["history"] = self.object.reigns.order_by('-start_date')
        return context
