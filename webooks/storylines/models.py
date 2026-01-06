from django.db import models
from booking.models import Match, Event
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Storyline(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class StorylinePoint(models.Model):
    storyline = models.ForeignKey(
        Storyline,
        on_delete=models.CASCADE,
        related_name="points"
    )

    # Can point to a Match or an Event
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    order_index = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["order_index"]

    def __str__(self):
        return f"{self.storyline} → {self.content_object}"
