from django.conf import settings
from django.db import models

from accounts.choices import VehicleType, ExperienceLevel


class Profile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = 'profile',
    )

    bio = models.TextField(
        max_length = 500,
        blank = True,
    )

    avatar = models.ImageField(
        upload_to = 'avatars/',
        blank = True,
        null = True,
    )

    vehicle_type = models.CharField(
        max_length = 20,
        choices = VehicleType.choices,
        default = VehicleType.FOURXFOUR,
    )

    riding_experience = models.CharField(
        max_length = 20,
        choices = ExperienceLevel.choices,
        default = ExperienceLevel.BEGINNER,
    )

    location = models.CharField(
        max_length = 100,
        blank = True,
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"