from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from titles.models import Championship, TitleReign
from core.forms import ChampionshipForm

# Championship Views

class ChampionshipListView(ListView):
    model = Championship
    template_name = "titles/championship_list.html"
    context_object_name = "championships"
    ordering = ['name']

class ChampionshipDetailView(DetailView):
    model = Championship
    template_name = "titles/championship_detail.html"
    context_object_name = "championship"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get current reign
        context["current_reign"] = self.object.current_reign()
        # All past reigns
        context["past_reigns"] = self.object.reigns.exclude(end_date__isnull=True)
        return context

class ChampionshipCreateView(CreateView):
    model = Championship
    form_class = ChampionshipForm
    template_name = "titles/championship_form.html"
    success_url = reverse_lazy("championship-list")

class ChampionshipUpdateView(UpdateView):
    model = Championship
    form_class = ChampionshipForm
    template_name = "titles/championship_form.html"
    success_url = reverse_lazy("championship-list")

class TitleReignDetailView(DetailView):
    model = TitleReign
    template_name = "titles/titlereign_detail.html"
    context_object_name = "reign"
