from django.shortcuts import render

from django.views.generic import ListView
from core.models import Character

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
