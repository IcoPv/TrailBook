from io import BytesIO

from PIL import Image
from celery import shared_task
from django.core.files.base import ContentFile


@shared_task(bind=True, max_retries=3)
def generate_thumbnail(self, photo_id):
    try:
        from gallery.models import Photo
        photo = Photo.objects.get(id=photo_id)

        if photo.is_thumbnail_generated:
            return f"Thumbnail for photo {photo_id} exists"

        original = photo.image.open()
        img = Image.open(original)
        img.thumbnail((400, 400))

        buffer = BytesIO()
        img_format = "JPEG"
        img.save(buffer, format=img_format, quality=85)
        buffer.seek(0)

        thumb_name = f"{photo.pk}_thumb.jpg"
        photo.thumbnail.save(thumb_name, ContentFile(buffer.read()), save=False)
        photo.is_thumbnail_generated = True
        photo.save(update_fields=['thumbnail', 'is_thumbnail_generated'])

        return f"Thumbnail generated for photo {photo_id}"

    except Photo.DoesNotExist:
        return f"Photo {photo_id} not found"
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)