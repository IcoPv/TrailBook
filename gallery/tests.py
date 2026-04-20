from datetime import date, timedelta
from io import BytesIO

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from gallery.forms import PhotoUploadForm
from gallery.models import Photo
from trips.models import Trip

User = get_user_model()



def create_test_image(size=(800, 600), format='JPEG'):

    buffer = BytesIO()
    image = Image.new('RGB', size, color='red')
    image.save(buffer, format=format)
    buffer.seek(0)
    return SimpleUploadedFile(
        f"test.{format.lower()}",
        buffer.read(),
        content_type = f"image/{format.lower()}"
    )




class PhotoUploadFormTests(TestCase):

    def setUp(self):

        user = User.objects.create_user(username='rider', password='pass')
        self.trip = Trip.objects.create(
            owner = user,
            title = 'Test Trip',
            description = '...',
            start_date = date.today(),
            end_date = date.today() + timedelta(days=1),
        )

    def test_form_rejects_oversized_file(self):

        big_data = b'x' * (6 * 1024 * 1024)
        big_file = SimpleUploadedFile(
            'big.jpg',
            big_data,
            content_type = 'image/jpeg',
        )

        form = PhotoUploadForm(
            data = {'caption': 'Test'},
            files = {'image': big_file},
            trip = self.trip,
        )

        self.assertFalse(form.is_valid())
        self.assertIn('image', form.errors)

    def test_form_rejects_invalid_content_type(self):

        bad_file = SimpleUploadedFile(
            'evil.exe',
            b'fake data',
            content_type = 'application/x-msdownload',
        )

        form = PhotoUploadForm(
            data = {'caption': 'Test'},
            files = {'image': bad_file},
            trip = self.trip,
        )

        self.assertFalse(form.is_valid())



@override_settings(CELERY_TASK_ALWAYS_EAGER=True, CELERY_TASK_EAGER_PROPAGATES=True)
class ThumbnailTaskTests(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(username='rider', password='pass')
        self.trip = Trip.objects.create(
            owner=self.user,
            title='Test Trip',
            description='...',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
        )

    def test_thumbnail_generation_creates_thumbnail(self):

        photo = Photo.objects.create(
            trip=self.trip,
            uploaded_by=self.user,
            image=create_test_image(),
            caption='Test',
        )
        photo.refresh_from_db()

        self.assertTrue(photo.is_thumbnail_generated)
        self.assertTrue(photo.thumbnail)