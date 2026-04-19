from django.conf import settings
from django.db import models



class TrailNote(models.Model):

    trip = models.ForeignKey(
        'trips.Trip',
        on_delete = models.CASCADE,
        related_name = 'trail_notes',
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = 'trail_notes',
    )

    body = models.TextField(
        max_length = 2000,
    )

    is_flagged = models.BooleanField(
        default = False,
    )

    created_at = models.DateTimeField(
        auto_now_add = True,
    )

    updated_at = models.DateTimeField(
        auto_now = True,
    )

    class Meta:
        ordering = ['created_at']
        permissions = [
            ('can_moderate_trail_notes', 'Can edit/delete any trail note'),
        ]

    def __str__(self):
        return f"Note by {self.author.username} on {self.trip.title}"



class Bookmark(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = 'bookmarks',
    )

    trip = models.ForeignKey(
        'trips.Trip',
        on_delete = models.CASCADE,
        related_name = 'bookmarks',
    )

    created_at = models.DateTimeField(
        auto_now_add = True,
    )

    class Meta:
        unique_together = [['user', 'trip']]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} bookmarked { self.trip.title}"