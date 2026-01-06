from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),  # Dashboard homepage at root
    path('characters/', include('core.urls')),
    path('shows/', include('booking.urls')),
    path('storylines/', include('storylines.urls')),
    path('titles/', include('titles.urls')),
]
