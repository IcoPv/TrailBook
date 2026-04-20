from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

from trips.models import Trip
from waypoints.models import Waypoint

User = get_user_model()



class WaypointModelTests(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(username='rider', password='pass')
        self.trip = Trip.objects.create(
            owner = self.user,
            title = 'Test Trip',
            description = '...',
            start_date = date(2026, 5, 1),
            end_date = date(2026, 5, 5),
        )

    def test_waypoint_clean_rejects_arrival_outside_trip(self):

        waypoint = Waypoint(
            trip = self.trip,
            name = 'Bad arrival',
            latitude = Decimal('42.0'),
            longitude = Decimal('23.0'),
            order = 1,
            arrival_date = date(2026, 6, 1),
        )
        with self.assertRaises(ValidationError):
            waypoint.clean()

    def test_waypoint_unique_together_enforced(self):

        Waypoint.objects.create(
            trip = self.trip,
            name = 'First',
            latitude = Decimal('42.0'),
            longitude = Decimal('23.0'),
            order = 1,
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Waypoint.objects.create(
                    trip = self.trip,
                    name = 'Duplicate order',
                    latitude = Decimal('43.0'),
                    longitude = Decimal('24.0'),
                    order = 1,
                )



class WaypointCreateViewTests(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(username='rider', password='pass')
        self.trip = Trip.objects.create(
            owner = self.user,
            title = 'Test Trip',
            description = '...',
            start_date = date(2026, 5, 1),
            end_date = date(2026, 5, 5),
        )

    def test_single_waypoint_create_sets_trip(self):

        self.client.login(username='rider', password='pass')
        response = self.client.post(
            reverse('trips:add_single_waypoint', kwargs={'slug': self.trip.slug}),
            {
                'name': 'Scenic overlook',
                'latitude': '42.697708',
                'longitude': '23.321867',
                'order': 1,
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Waypoint.objects.filter(trip=self.trip, name='Scenic overlook').exists())

