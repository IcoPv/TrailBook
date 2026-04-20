from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError

from trips.forms import TripForm
from trips.models import Trip

User = get_user_model()



class TripModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='rider1', password='pass')

    def test_trip_str_representation(self):
        trip = Trip.objects.create(
            owner = self.user,
            title = 'Rila Loop',
            description = 'A great ride, through the mountain',
            start_date = date.today(),
            end_date = date.today() + timedelta(days=2),
        )
        self.assertEqual(str(trip), 'Rila Loop')

    def test_trip_clean_rejects_end_before_start(self):
        trip = Trip(
            owner = self.user,
            title = 'Bad dates',
            description = '...',
            start_date = date(2026, 5, 10),
            end_date = date(2026, 5, 5),
        )
        with self.assertRaises(ValidationError):
            trip.clean()

    def test_trip_duration_days(self):
        trip = Trip.objects.create(
            owner=self.user,
            title='Three day ride',
            description='...',
            start_date=date(2026, 5, 1),
            end_date=date(2026, 5, 3),
        )
        self.assertEqual(trip.duration_days, 3)



class TripFormTests(TestCase):

    def test_form_rejects_end_before_start(self):
        form = TripForm(data={
            'title': 'Trip with bad dates',
            'description': '...',
            'difficulty': 'moderate',
            'vehicle_type': '4x4',
            'start_date': '2026-05-10',
            'end_date': '2026-05-01',
        })
        self.assertFalse(form.is_valid())



class TripViewTests(TestCase):

    def setUp(self):

        Group.objects.get_or_create(name='Rider')
        self.owner = User.objects.create_user(username='owner', password='pass')
        self.other = User.objects.create_user(username='other', password='pass')
        self.trip = Trip.objects.create(
            owner = self.owner,
            title = 'Owner Trip',
            description = '...',
            start_date = date.today(),
            end_date = date.today() + timedelta(days=1),
        )

    def test_trip_create_requires_login(self):

        response = self.client.get(reverse('trips:create_trip'))
        self.assertEqual(response.status_code, 302)

    def test_non_owner_cannot_edit_trip(self):

        self.client.login(username='other', password='pass')
        response = self.client.get(
            reverse('trips:update_trip', kwargs={'slug': self.trip.slug})
        )
        self.assertEqual(response.status_code, 404)

    def test_owner_can_access_edit(self):

        self.client.login(username='owner', password='pass')
        response = self.client.get(
            reverse('trips:update_trip', kwargs={'slug': self.trip.slug})
        )
        self.assertEqual(response.status_code, 200)

