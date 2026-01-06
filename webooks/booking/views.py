from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from booking.models import Show, Match, MatchParticipant, Event, EventParticipant
from booking.forms import MatchSimulationForm
from core.models import Character
from titles.models import TitleReign

# Show List
class ShowListView(ListView):
    model = Show
    template_name = "booking/show_list.html"
    context_object_name = "shows"
    ordering = ['-airing_date']
    paginate_by = 20

# Show Detail
class ShowDetailView(DetailView):
    model = Show
    template_name = "booking/show_detail.html"
    context_object_name = "show"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        show = self.object
        context["matches"] = show.match_set.all()
        context["events"] = show.event_set.all()
        return context

# Show Create
class ShowCreateView(CreateView):
    model = Show
    template_name = "booking/show_form.html"
    fields = ["title", "show_type", "episode_number", "airing_date", "filmed", "uploaded", "youtube_link"]
    success_url = reverse_lazy("show-list")

# Show Update
class ShowUpdateView(UpdateView):
    model = Show
    template_name = "booking/show_form.html"
    fields = ["title", "show_type", "episode_number", "airing_date", "filmed", "uploaded", "youtube_link"]
    success_url = reverse_lazy("show-list")

# Match Detail
class MatchDetailView(DetailView):
    model = Match
    template_name = "booking/match_detail.html"
    context_object_name = "match"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        match = self.object
        # All participants in this match
        context["participants"] = match.matchparticipant_set.all()
        return context

# Match Create
class MatchCreateView(CreateView):
    model = Match
    template_name = "booking/match_form.html"
    fields = ["show", "title", "match_type", "stipulation", "championship", "notes"]
    success_url = reverse_lazy("show-list")

# Match Update
class MatchUpdateView(UpdateView):
    model = Match
    template_name = "booking/match_form.html"
    fields = ["show", "title", "match_type", "stipulation", "championship", "notes"]
    success_url = reverse_lazy("show-list")
    

class MatchParticipantCreateView(CreateView):
    model = MatchParticipant
    template_name = "booking/matchparticipant_form.html"
    fields = ["match", "character", "side", "won"]
    
    def get_initial(self):
        # Pre-fill the match if coming from match detail page
        match_id = self.kwargs.get("match_id")
        return {"match": match_id} if match_id else {}

    def get_success_url(self):
        return reverse_lazy("match-detail", kwargs={"pk": self.object.match.id})


class MatchParticipantUpdateView(UpdateView):
    model = MatchParticipant
    template_name = "booking/matchparticipant_form.html"
    fields = ["match", "character", "side", "won"]

    def get_success_url(self):
        return reverse_lazy("match-detail", kwargs={"pk": self.object.match.id})

# Event Detail
class EventDetailView(DetailView):
    model = Event
    template_name = "booking/event_detail.html"
    context_object_name = "event"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.object
        # All participants for this event
        context["participants"] = event.eventparticipant_set.all()
        return context

# Event Create
class EventCreateView(CreateView):
    model = Event
    template_name = "booking/event_form.html"
    fields = ["show", "title", "event_type", "short_description"]
    success_url = reverse_lazy("show-list")

# Event Update
class EventUpdateView(UpdateView):
    model = Event
    template_name = "booking/event_form.html"
    fields = ["show", "title", "event_type", "short_description"]
    success_url = reverse_lazy("show-list")

class EventParticipantCreateView(CreateView):
    model = EventParticipant
    template_name = "booking/eventparticipant_form.html"
    fields = ["event", "character", "role"]

    def get_initial(self):
        # Pre-fill the event if coming from event detail page
        event_id = self.kwargs.get("event_id")
        return {"event": event_id} if event_id else {}

    def get_success_url(self):
        return reverse_lazy("event-detail", kwargs={"pk": self.object.event.id})


class EventParticipantUpdateView(UpdateView):
    model = EventParticipant
    template_name = "booking/eventparticipant_form.html"
    fields = ["event", "character", "role"]

    def get_success_url(self):
        return reverse_lazy("event-detail", kwargs={"pk": self.object.event.id})

def simulate_match(request, pk):
    match = get_object_or_404(Match, pk=pk)
    participants = match.matchparticipant_set.all()

    if request.method == "POST":
        form = MatchSimulationForm(request.POST, match=match)
        if form.is_valid():
            # Reset all participants' won status first
            participants.update(won=False)
            winners = form.cleaned_data["winners"]
            winners.update(won=True)
            
            # Save match finish
            match.finish = form.cleaned_data["finish"]
            match.save()

            # Handle championship title changes
            if match.championship:
                # End current reign(s)
                TitleReign.objects.filter(
                    championship=match.championship,
                    end_date__isnull=True
                ).update(end_date=match.show.airing_date)
                
                # Create new reign(s)
                for winner in winners:
                    TitleReign.objects.create(
                        championship=match.championship,
                        character=winner.character,
                        start_date=match.show.airing_date
                    )
            
            # Redirect back to show detail instead of match detail
            return redirect("show-detail", pk=match.show.id)
    else:
        form = MatchSimulationForm(match=match)

    return render(request, "booking/simulate_match.html", {"match": match, "form": form})

