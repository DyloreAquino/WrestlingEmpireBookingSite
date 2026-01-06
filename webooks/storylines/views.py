from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from storylines.models import Storyline, StorylinePoint
from storylines.forms import AddMatchToStorylineForm, AddEventToStorylineForm
from booking.models import Match, Event
from django.contrib.contenttypes.models import ContentType

# Storyline List
class StorylineListView(ListView):
    model = Storyline
    template_name = "storylines/storyline_list.html"
    context_object_name = "storylines"
    ordering = ['title']

# Storyline Detail
class StorylineDetailView(DetailView):
    model = Storyline
    template_name = "storylines/storyline_detail.html"
    context_object_name = "storyline"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        storyline = self.object
        context["matches"] = storyline.matches.all()
        context["events"] = storyline.events.all()
        return context

# Storyline Create
class StorylineCreateView(CreateView):
    model = Storyline
    template_name = "storylines/storyline_form.html"
    fields = ["title", "summary"]
    success_url = reverse_lazy("storyline-list")

# Storyline Update
class StorylineUpdateView(UpdateView):
    model = Storyline
    template_name = "storylines/storyline_form.html"
    fields = ["title", "summary"]
    success_url = reverse_lazy("storyline-list")

def add_match_to_storyline(request, pk):
    storyline = get_object_or_404(Storyline, pk=pk)
    match_ct = ContentType.objects.get_for_model(Match)

    # Exclude matches already in this storyline
    used_match_ids = StorylinePoint.objects.filter(
        storyline=storyline,
        content_type=match_ct
    ).values_list('object_id', flat=True)

    available_matches = Match.objects.exclude(id__in=used_match_ids)

    if request.method == "POST":
        form = AddMatchToStorylineForm(request.POST, available_matches=available_matches)
        if form.is_valid():
            match = form.cleaned_data['match']
            StorylinePoint.objects.create(
                storyline=storyline,
                content_type=match_ct,
                object_id=match.id
            )
            return redirect("storyline-detail", pk=storyline.pk)
    else:
        form = AddMatchToStorylineForm(available_matches=available_matches)

    return render(request, "storylines/add_match_to_storyline.html", {
        "storyline": storyline,
        "form": form
    })

def add_event_to_storyline(request, pk):
    storyline = get_object_or_404(Storyline, pk=pk)
    
    if request.method == "POST":
        form = AddEventToStorylineForm(request.POST)
        if form.is_valid():
            event = form.cleaned_data["event"]
            storyline.events.add(event)
            return redirect("storyline-detail", pk=storyline.id)
    else:
        form = AddEventToStorylineForm()
        form.fields["event"].queryset = Event.objects.exclude(storylines=storyline)

    return render(request, "storylines/add_event_to_storyline.html", {"form": form, "storyline": storyline})
