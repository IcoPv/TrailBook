from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from autoslug import AutoSlugField

from trips.choices import Difficulty, VehicleTypeTrips


class Tag(models.Model):

    name = models.CharField(
        max_length = 50,
        unique = True,
    )

    slug = models.SlugField(
        max_length = 50,
        unique = True,
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Trip(models.Model):

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = 'trips',
    )

    tags = models.ManyToManyField(
        'Tag',
        blank = True,
        related_name = 'trips',
    )

    title = models.CharField(
        max_length = 100,
    )

    slug = AutoSlugField(
        populate_from = 'title',
        unique = True,
    )

    description = models.TextField(
        max_length = 500,
    )

    difficulty = models.CharField(
        max_length = 20,
        choices = Difficulty.choices,
        default = Difficulty.MODERATE,
    )

    vehicle_type = models.CharField(
        max_length = 20,
        choices = VehicleTypeTrips.choices,
        default = VehicleTypeTrips.FOURXFOUR,
    )

    start_date = models.DateField()

    end_date = models.DateField()

    is_featured = models.BooleanField(
        default = False,
    )

    created_at = models.DateTimeField(
        auto_now_add = True,
    )

    updated_at = models.DateTimeField(
        auto_now = True,
    )

    class Meta:
        ordering = ['-created_at']
        permissions = [
            ('can_feature_trips', 'Can feature/unfeature trips'),
        ]

    def __str__(self):
        return self.title

    def clean(self):

        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError({
                'end_date': 'End date cannot be before start date.'
            })

    @property
    def duration_days(self):
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days + 1
        return None