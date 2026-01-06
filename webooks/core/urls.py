from django.urls import path
from core.views import CharacterListView

urlpatterns = [
    path("characters/", CharacterListView.as_view(), name="character-list"),
]
