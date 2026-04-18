from django.db.models.signals import post_save
from django.dispatch import receiver

from gallery.models import Photo
from gallery.tasks import generate_thumbnail


@receiver(post_save, sender=Photo)
def trigger_thumbnail_generation(sender, instance, created, **kwargs):
    if created and not instance.is_thumbnail_generated:
        generate_thumbnail.delay(instance.pk)