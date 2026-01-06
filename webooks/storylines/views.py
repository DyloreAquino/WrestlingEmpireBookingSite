from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from storylines.models import Storyline
from storylines.forms import AddMatchToStorylineForm, AddEventToStorylineForm
from booking.models import Match, Event

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
    
    if request.method == "POST":
        form = AddMatchToStorylineForm(request.POST)
        if form.is_valid():
            match = form.cleaned_data["match"]
            storyline.matches.add(match)
            return redirect("storyline-detail", pk=storyline.id)
    else:
        # Exclude matches already in this storyline
        form = AddMatchToStorylineForm()
        form.fields["match"].queryset = Match.objects.exclude(storylines=storyline)

    return render(request, "storylines/add_match_to_storyline.html", {"form": form, "storyline": storyline})


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
