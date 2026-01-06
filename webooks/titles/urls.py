from django.urls import path
from titles.views import (
    ChampionshipListView, ChampionshipDetailView,
    ChampionshipCreateView, ChampionshipUpdateView,
    TitleReignDetailView
)

urlpatterns = [
    path("", ChampionshipListView.as_view(), name="championship-list"),
    path("add/", ChampionshipCreateView.as_view(), name="championship-add"),
    path("<int:pk>/", ChampionshipDetailView.as_view(), name="championship-detail"),
    path("<int:pk>/edit/", ChampionshipUpdateView.as_view(), name="championship-edit"),
    
    path("reign/<int:pk>/", TitleReignDetailView.as_view(), name="titlereign-detail"),
]
