from django.shortcuts import render

from django.views.generic import ListView, DetailView, CreateView, UpdateView
from core.models import Character, Group, Championship
from core.forms import CharacterForm
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

        # Storyline points (optional)
        context["storyline_points"] = character.storylinepoint_set.all() if hasattr(character, 'storylinepoint_set') else []

        return context

class CharacterCreateView(CreateView):
    model = Character
    form_class = CharacterForm
    template_name = "core/character_form.html"
    success_url = reverse_lazy("character-list")

class CharacterUpdateView(UpdateView):
    model = Character
    form_class = CharacterForm
    template_name = "core/character_form.html"
    success_url = reverse_lazy("character-list")


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
    template_name = "core/group_form.html"
    fields = ["name", "group_type", "active", "members"]
    success_url = reverse_lazy("group-list")

class GroupUpdateView(UpdateView):
    model = Group
    template_name = "core/group_form.html"
    fields = ["name", "group_type", "active", "members"]
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
        context["current_reigns"] = self.object.titlereign_set.filter(end_date__isnull=True)
        # Full title history
        context["history"] = self.object.titlereign_set.order_by('-start_date')
        return context
