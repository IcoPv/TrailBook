from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase

from trips.models import Trip

User = get_user_model()



class TripApiTests(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(username='rider', password='pass')

        self.trip_easy = Trip.objects.create(
            owner = self.user,
            title = 'Easy Trip',
            description = '...',
            difficulty = 'easy',
            vehicle_type = 'motorcycle',
            start_date = date.today(),
            end_date = date.today() + timedelta(days=1),
        )

        self.trip_hard = Trip.objects.create(
            owner = self.user,
            title = 'Hard Trip',
            description = '...',
            difficulty = 'extreme',
            vehicle_type = '4x4',
            start_date = date.today(),
            end_date = date.today() + timedelta(days=2),
        )

    def test_api_trips_list_returns_200(self):

        response = self.client.get('/api/trips/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 2)

    def test_api_filters_by_difficulty(self):

        response = self.client.get('/api/trips/?difficulty=easy')

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data['count'], 1)
        self.assertEqual(data['results'][0]['title'], 'Easy Trip')

    def test_api_detail_includes_waypoints(self):

        response = self.client.get(f'/api/trips/{self.trip_easy.slug}/')

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertIn('waypoints', data)
        self.assertIn('description', data)