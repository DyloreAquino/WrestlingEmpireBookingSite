from django.urls import path
from dashboard.views import homepage

urlpatterns = [
    path("", homepage, name="homepage"),
]
