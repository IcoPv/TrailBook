from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models



class WaypointCategory(models.Model):

    name = models.CharField(
        max_length = 50,
        unique = True,
    )

    slug = models.SlugField(
        max_length = 50,
        unique = True,
    )

    icon = models.CharField(
        max_length = 50,
        blank = True,
        null = True,
        help_text = 'CSS icon class, e.g. bi-fuel-pump (for future Leaflet markers)'
    )

    class Meta:
        verbose_name_plural = 'Waypoint Categories'
        ordering = ['name']

    def __str__(self):
        return self.name





class Waypoint(models.Model):

    trip = models.ForeignKey(
        'trips.Trip',
        on_delete = models.CASCADE,
        related_name = 'waypoints',
    )

    name = models.CharField(
        max_length = 100,
    )

    description = models.TextField(
        max_length = 500,
        blank = True,
        null = True,
    )

    latitude = models.DecimalField(
        max_digits = 9,
        decimal_places = 6,
        validators = [
            MinValueValidator(-90),
            MaxValueValidator(90)
        ],
        help_text = 'Latitude in decimal degrees, up to 6 decimal spaces (range: -90 to 90)'
    )

    longitude = models.DecimalField(
        max_digits = 9,
        decimal_places = 6,
        validators = [
            MinValueValidator(-180),
            MaxValueValidator(180)
        ],
        help_text = 'Longitude in decimal degrees, up to 6 decimal spaces (range: -180 to 180)'
    )

    elevation = models.IntegerField(
        blank = True,
        null = True,
        help_text = 'Elevation in meters'
    )

    categories = models.ManyToManyField(
        'WaypointCategory',
        blank = True,
        related_name = 'waypoints',
    )

    order = models.PositiveIntegerField(
        help_text = 'Display order within the trip'
    )

    arrival_date = models.DateField(
        blank = True,
        null = True,
    )

    class Meta:
        ordering = ['order']
        unique_together = [['trip', 'order']]

    def __str__(self):
        return f"{self.order}. {self.name}"

    def clean(self):
        if self.arrival_date and self.trip_id:
            trip = self.trip
            if self.arrival_date < trip.start_date or self.arrival_date > trip.end_date:
                raise ValidationError({
                    'arrival_date': 'Arrival date must be within the trip date range.'
                })