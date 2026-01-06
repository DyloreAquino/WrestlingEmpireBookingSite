from django.urls import path
from storylines.views import (
    StorylineListView, StorylineDetailView,
    StorylineCreateView, StorylineUpdateView
)
from storylines.views import add_match_to_storyline, add_event_to_storyline

urlpatterns = [
    path("", StorylineListView.as_view(), name="storyline-list"),
    path("add/", StorylineCreateView.as_view(), name="storyline-add"),
    path("<int:pk>/", StorylineDetailView.as_view(), name="storyline-detail"),
    path("<int:pk>/edit/", StorylineUpdateView.as_view(), name="storyline-edit"),
]

urlpatterns += [
    path("<int:pk>/add-match/", add_match_to_storyline, name="storyline-add-match"),
    path("<int:pk>/add-event/", add_event_to_storyline, name="storyline-add-event"),
]
