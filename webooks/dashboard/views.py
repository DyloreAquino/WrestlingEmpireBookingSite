from django.shortcuts import render
from booking.models import Show
from titles.models import Championship

def homepage(request):
    # Last aired show
    last_show = Show.objects.filter(is_filmed=True).order_by('-airing_date').first()
    last_show_matches = last_show.match_set.all() if last_show else []

    # Current champions
    championships = Championship.objects.all()
    current_champions = {}
    for champ in championships:
        reign = champ.current_reign()  # method in Championship model
        current_champions[champ] = reign.character if reign else None

    context = {
        "last_show": last_show,
        "last_show_matches": last_show_matches,
        "current_champions": current_champions,
    }
    return render(request, "dashboard/homepage.html", context)
