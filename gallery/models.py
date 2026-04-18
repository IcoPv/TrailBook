from django.db import models

from django.conf import settings


class Photo(models.Model):

    trip = models.ForeignKey(
        'trips.Trip',
        on_delete = models.CASCADE,
        related_name = 'photos',
    )

    waypoint = models.ForeignKey(
        'waypoints.Waypoint',
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
        related_name = 'photos',
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = 'photos',
    )

    image = models.ImageField(
        upload_to = 'photos/%Y/%m/'
    )

    thumbnail = models.ImageField(
        upload_to = 'photos/thumb/%Y/%m/',
        blank = True,
        null = True,
    )

    caption = models.CharField(
        max_length = 300,
        blank = True,
    )

    is_thumbnail_generated = models.BooleanField(
        default = False,
    )

    uploaded_at = models.DateTimeField(
        auto_now_add = True,
    )

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Photo for {self.trip.title} ({self.pk})"
