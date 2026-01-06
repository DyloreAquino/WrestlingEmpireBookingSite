from django.urls import path
from core.views import CharacterListView, CharacterDetailView, CharacterCreateView, CharacterUpdateView
from core.views import GroupListView, GroupDetailView, GroupCreateView, GroupUpdateView
from core.views import ChampionshipListView, ChampionshipDetailView

urlpatterns = [
    path("characters/", CharacterListView.as_view(), name="character-list"),
    path("characters/<int:pk>/", CharacterDetailView.as_view(), name="character-detail"),
    path("characters/add/", CharacterCreateView.as_view(), name="character-add"),
    path("characters/<int:pk>/edit/", CharacterUpdateView.as_view(), name="character-edit"),
]

urlpatterns += [
    path("groups/", GroupListView.as_view(), name="group-list"),
    path("groups/<int:pk>/", GroupDetailView.as_view(), name="group-detail"),
    path("groups/add/", GroupCreateView.as_view(), name="group-add"),
    path("groups/<int:pk>/edit/", GroupUpdateView.as_view(), name="group-edit"),
]

urlpatterns += [
    path("championships/", ChampionshipListView.as_view(), name="championship-list"),
    path("championships/<int:pk>/", ChampionshipDetailView.as_view(), name="championship-detail"),
]
