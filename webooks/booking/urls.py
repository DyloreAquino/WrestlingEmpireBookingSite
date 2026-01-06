from django.urls import path
from booking.views import ShowListView, ShowDetailView, ShowCreateView, ShowUpdateView, simulate_match
from booking.views import MatchDetailView, MatchCreateView, MatchUpdateView
from booking.views import MatchParticipantCreateView, MatchParticipantUpdateView
from booking.views import EventDetailView, EventCreateView, EventUpdateView
from booking.views import EventParticipantCreateView, EventParticipantUpdateView

urlpatterns = [
    path("shows/", ShowListView.as_view(), name="show-list"),
    path("shows/add/", ShowCreateView.as_view(), name="show-add"),
    path("shows/<int:pk>/", ShowDetailView.as_view(), name="show-detail"),
    path("shows/<int:pk>/edit/", ShowUpdateView.as_view(), name="show-edit"),
]

urlpatterns += [
    path(
        "shows/<int:show_id>/matches/add/",
        MatchCreateView.as_view(),
        name="match-add",
    ),
    path("matches/<int:pk>/", MatchDetailView.as_view(), name="match-detail"),
    path("matches/<int:pk>/edit/", MatchUpdateView.as_view(), name="match-edit"),
]

urlpatterns += [
    path(
        "matches/<int:match_id>/participants/add/",
        MatchParticipantCreateView.as_view(),
        name="matchparticipant-add",
    ),
    path(
        "participants/<int:pk>/edit/",
        MatchParticipantUpdateView.as_view(),
        name="matchparticipant-edit",
    ),
]

urlpatterns += [
    path(
        "shows/<int:show_id>/events/add/",
        EventCreateView.as_view(),
        name="event-add",
    ),
    path("events/<int:pk>/", EventDetailView.as_view(), name="event-detail"),
    path("events/<int:pk>/edit/", EventUpdateView.as_view(), name="event-edit"),
]

urlpatterns += [
    path(
        "events/<int:event_id>/participants/add/",
        EventParticipantCreateView.as_view(),
        name="eventparticipant-add",
    ),
    path(
        "eventparticipants/<int:pk>/edit/",
        EventParticipantUpdateView.as_view(),
        name="eventparticipant-edit",
    ),
]

urlpatterns += [
    path("matches/<int:pk>/simulate/", simulate_match, name="match-simulate"),
]