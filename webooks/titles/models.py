from django.db import models
from core.models import Championship, Character, Group
from booking.models import Match

class TitleReign(models.Model):
    championship = models.ForeignKey(
        Championship,
        on_delete=models.CASCADE,
        related_name="reigns"
    )

    # Either a solo champion or a group (for tag teams)
    character = models.ForeignKey(
        Character,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="title_reigns"
    )
    group = models.ForeignKey(
        Group,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="title_reigns"
    )

    # The match in which the title was won
    won_in_match = models.ForeignKey(
        Match,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="title_changes"
    )

    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)  # null if still champion

    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        holder = self.character or self.group
        return f"{holder} — {self.championship.name}"
