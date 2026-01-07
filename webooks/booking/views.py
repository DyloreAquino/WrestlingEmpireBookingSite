from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from booking.models import Show, Match, MatchParticipant, Event, EventParticipant
from booking.forms import MatchSimulationForm, ShowForm, MatchForm, MatchParticipantForm, EventForm, EventParticipantForm
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
        context["matches"] = show.matches.all()
        context["events"] = show.events.all()
        return context

# Show Create
class ShowCreateView(CreateView):
    model = Show
    form_class = ShowForm
    template_name = "booking/show_form.html"
    success_url = reverse_lazy("show-list")

# Show Update
class ShowUpdateView(UpdateView):
    model = Show
    form_class = ShowForm
    template_name = "booking/show_form.html"
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
        context["participants"] = match.participants.all()
        return context

class MatchCreateView(CreateView):
    model = Match
    form_class = MatchForm
    template_name = "booking/match_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["show"] = Show.objects.get(pk=self.kwargs["show_id"])
        return context

    def form_valid(self, form):
        show = Show.objects.get(pk=self.kwargs["show_id"])
        form.instance.show = show
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("show-detail", kwargs={"pk": self.object.show.id})


# Match Update
class MatchUpdateView(UpdateView):
    model = Match
    form_class = MatchForm
    template_name = "booking/match_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the show explicitly to the template
        context["show"] = self.object.show
        return context

    def get_success_url(self):
        return reverse("show-detail", kwargs={"pk": self.object.show.pk})
    

class MatchParticipantCreateView(CreateView):
    model = MatchParticipant
    form_class = MatchParticipantForm
    template_name = "booking/matchparticipant_form.html"
    
    def get_initial(self):
        # Pre-fill the match if coming from match detail page
        match_id = self.kwargs.get("match_id")
        return {"match": match_id} if match_id else {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the match to the template
        context['match'] = Match.objects.get(pk=self.kwargs['match_id'])
        return context

    def form_valid(self, form):
        # Assign the match before saving
        match = Match.objects.get(pk=self.kwargs['match_id'])
        form.instance.match = match
        return super().form_valid(form)

    def get_success_url(self):
        # After saving, go back to match detail
        return reverse("match-detail", kwargs={"pk": self.object.match.pk})


class MatchParticipantUpdateView(UpdateView):
    model = MatchParticipant
    form_class = MatchParticipantForm
    template_name = "booking/matchparticipant_form.html"

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
        context["participants"] = event.participants.all()
        return context

# Event Create
class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = "booking/event_form.html"
    success_url = reverse_lazy("show-list")

# Event Update
class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = "booking/event_form.html"
    success_url = reverse_lazy("show-list")

class EventParticipantCreateView(CreateView):
    model = EventParticipant
    form_class = EventParticipantForm
    template_name = "booking/eventparticipant_form.html"

    def get_initial(self):
        # Pre-fill the event if coming from event detail page
        event_id = self.kwargs.get("event_id")
        return {"event": event_id} if event_id else {}

    def get_success_url(self):
        return reverse_lazy("event-detail", kwargs={"pk": self.object.event.id})


class EventParticipantUpdateView(UpdateView):
    model = EventParticipant
    form_class = EventParticipantForm
    template_name = "booking/eventparticipant_form.html"

    def get_success_url(self):
        return reverse_lazy("event-detail", kwargs={"pk": self.object.event.id})

def simulate_match(request, pk):
    match = get_object_or_404(Match, pk=pk)
    participants = match.participants.all()

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

