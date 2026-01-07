from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from core.models import Character, Group, Championship

class Show(models.Model):
    class ShowType(models.TextChoices):
        WEEKLY = "WEEKLY", "Weekly"
        PLE = "PLE", "PLE"
        SPECIAL = "SPECIAL", "Special"

    title = models.CharField(max_length=200)
    show_type = models.CharField(max_length=20, choices=ShowType.choices)
    episode_number = models.PositiveIntegerField(null=True, blank=True)
    airing_date = models.DateField()

    is_filmed = models.BooleanField(default=False)
    is_uploaded = models.BooleanField(default=False)
    youtube_link = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.airing_date})"

class Stipulation(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Match(models.Model):
    class MatchType(models.TextChoices):
        SINGLES = "SINGLES", "Singles"
        TAG = "TAG", "Tag Team"
        TEAM = "TEAM", "Team"
        TRIPLE = "TRIPLE", "Triple Threat"
        FATAL_FOUR = "FATAL_FOUR", "Fatal Four-Way"
        HANDICAP = "HANDICAP", "Handicap"
        GAUNTLET = "GAUNTLET", "Gauntlet"
        BATTLE_ROYALE = "BATTLE_ROYALE", "Battle Royale"
        ROYAL_RUMBLE = "ROYAL_RUMBLE", "Royal Rumble"

    show = models.ForeignKey(
        "booking.Show",
        on_delete=models.CASCADE,
        related_name="matches"
    )

    title = models.CharField(max_length=200)
    match_type = models.CharField(max_length=30, choices=MatchType.choices)
    stipulations = models.ManyToManyField(
        Stipulation,
        blank=True,
        related_name="matches"
    )

    championship = models.ForeignKey(
        Championship, null=True, blank=True, on_delete=models.SET_NULL
    )

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def finish(self):
        """Return the human-readable finish label from the related MatchResult, or None if not recorded."""
        try:
            return self.result.get_finish_type_display()
        except Exception:
            return None


class MatchParticipant(models.Model):
    class Role(models.TextChoices):
        COMPETITOR = "COMPETITOR", "Competitor"
        MANAGER = "MANAGER", "Manager"
        REFEREE = "REFEREE", "Referee"
        INTERFERENCE = "INTERFERENCE", "Interference"

    class Side(models.TextChoices):
        TEAM_A = "TEAM_A", "Team A"
        TEAM_B = "TEAM_B", "Team B"
        SOLO = "SOLO", "Solo"

    match = models.ForeignKey(
        Match, on_delete=models.CASCADE, related_name="participants"
    )

    character = models.ForeignKey(
        Character, null=True, blank=True, on_delete=models.CASCADE
    )
    group = models.ForeignKey(
        Group, null=True, blank=True, on_delete=models.CASCADE
    )

    role = models.CharField(max_length=20, choices=Role.choices)
    side = models.CharField(
        max_length=10,
        choices=Side.choices,
        default=Side.SOLO
    )

    won = models.BooleanField(default=False)

    def __str__(self):
        target = self.character or self.group
        return f"{target} ({self.side}) in {self.match}"

class MatchResult(models.Model):
    class FinishType(models.TextChoices):
        PINFALL = "PINFALL", "Pinfall"
        SUBMISSION = "SUBMISSION", "Submission"
        COUNTOUT = "COUNTOUT", "Countout"
        DQ = "DQ", "Disqualification"
        UNIQUE = "UNIQUE", "Unique"
        NO_FINISH = "NO_FINISH", "No Finish"

    match = models.OneToOneField(
        Match, on_delete=models.CASCADE, related_name="result"
    )

    finish_type = models.CharField(max_length=20, choices=FinishType.choices)
    is_no_contest = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result of {self.match}"

class Event(models.Model):
    class EventType(models.TextChoices):
        PROMO = "PROMO", "Promo"
        CONFRONTATION = "CONFRONTATION", "Confrontation"
        TRAINING = "TRAINING", "Training"
        SEGMENT = "SEGMENT", "Segment"
        INJURY = "INJURY", "Injury"
        TURN = "TURN", "Turn"
        
    show = models.ForeignKey(
        "booking.Show",
        on_delete=models.CASCADE,
        related_name="events"
    )

    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=30, choices=EventType.choices)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class EventParticipant(models.Model):
    class Role(models.TextChoices):
        INITIATOR = "INITIATOR", "Initiator"
        INTERFERENCE = "INTERFERENCE", "Interference"
        VICTIM = "VICTIM", "Victim"
        ATTACKER = "ATTACKER", "Attacker"

    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="participants"
    )

    character = models.ForeignKey(
        Character, null=True, blank=True, on_delete=models.CASCADE
    )
    group = models.ForeignKey(
        Group, null=True, blank=True, on_delete=models.CASCADE
    )

    role = models.CharField(max_length=20, choices=Role.choices, blank=True)

    def __str__(self):
        target = self.character or self.group
        return f"{target} in {self.event}"

class ShowItem(models.Model):
    show = models.ForeignKey(
        Show, on_delete=models.CASCADE, related_name="items"
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    order_index = models.PositiveIntegerField()

    class Meta:
        ordering = ["order_index"]

    def __str__(self):
        return f"{self.show} item #{self.order_index}"
