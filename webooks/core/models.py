from django.db import models


class Character(models.Model):
    class Role(models.TextChoices):
        WRESTLER = "WRESTLER", "Wrestler"
        MANAGER = "MANAGER", "Manager"
        REFEREE = "REFEREE", "Referee"
        BOOKER = "BOOKER", "Booker"

    class Gender(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"
        NA = "NA", "N/A"

    class Alignment(models.TextChoices):
        FACE = "FACE", "Face"
        HEEL = "HEEL", "Heel"
        TWEENER = "TWEENER", "Tweener"

    ring_name = models.CharField(max_length=100, unique=True)
    role = models.CharField(max_length=20, choices=Role.choices)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    alignment = models.CharField(max_length=10, choices=Alignment.choices)

    finisher = models.CharField(max_length=100, blank=True)
    active = models.BooleanField(default=True)
    injured = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ring_name

class Group(models.Model):
    class GroupType(models.TextChoices):
        TAG = "TAG", "Tag Team"
        STABLE = "STABLE", "Stable"

    name = models.CharField(max_length=100, unique=True)
    group_type = models.CharField(max_length=10, choices=GroupType.choices)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="members")
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    role_in_group = models.CharField(max_length=50, blank=True)

    class Meta:
        unique_together = ("group", "character")

    def __str__(self):
        return f"{self.character} in {self.group}"

class CharacterRelationship(models.Model):
    class RelationshipType(models.TextChoices):
        FRIEND = "FRIEND", "Friend"
        ENEMY = "ENEMY", "Enemy"
        MANAGER = "MANAGER", "Manager"

    character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name="relationships"
    )
    related_character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name="related_to"
    )
    relationship_type = models.CharField(
        max_length=20,
        choices=RelationshipType.choices
    )

    class Meta:
        unique_together = ("character", "related_character", "relationship_type")

    def __str__(self):
        return f"{self.character} → {self.relationship_type} → {self.related_character}"

class Championship(models.Model):
    class Eligibility(models.TextChoices):
        MEN = "MEN", "Men Only"
        WOMEN = "WOMEN", "Women Only"
        OPEN = "OPEN", "Men & Women"

    name = models.CharField(max_length=100, unique=True)
    eligibility = models.CharField(
        max_length=10,
        choices=Eligibility.choices
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

