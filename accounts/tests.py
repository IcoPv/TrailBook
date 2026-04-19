from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from accounts.forms import RegistrationForm
from accounts.models import Profile

User = get_user_model()



class ProfileModelTests(TestCase):
    """Profile is auto-created via post_save signal on User."""

    def test_profile_is_created_with_user(self):
        user = User.objects.create_user(username='rider1', password='testpass123')
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_profile_str_representation(self):
        user = User.objects.create_user(username='rider1', password='testpass123')
        self.assertEqual(str(user.profile), "rider1's Profile")



class RegistrationFormTests(TestCase):

    def test_valid_form(self):

        form = RegistrationForm(data={
            'username': 'newrider',
            'email': 'new@rider.com',
            'first_name': 'New',
            'last_name': 'Rider',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        })

        self.assertTrue(form.is_valid())

    def test_duplicate_email_rejected(self):

        User.objects.create_user(
            username = 'existing',
            email = 'taken@rider.com',
            password = 'pass',
        )

        form = RegistrationForm(data={
            'username': 'newrider',
            'email': 'taken@rider.com',
            'first_name': 'New',
            'last_name': 'Rider',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)



class RegisterViewTests(TestCase):

    def setUp(self):
        # Ensure the rider group exists for the test DB
        Group.objects.get_or_create(name='Rider')

    def test_new_user_is_added_to_rider_group(self):

        self.client.post(reverse('accounts:register'), {
            'username': 'newrider',
            'email': 'new@rider.com',
            'first_name': 'New',
            'last_name': 'Rider',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        })

        user = User.objects.get(username='newrider')
        self.assertTrue(user.groups.filter(name='Rider').exists())



class ProfileEditViewTests(TestCase):

    def test_profile_edit_requires_login(self):

        response = self.client.get(reverse('accounts:profile_edit'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)