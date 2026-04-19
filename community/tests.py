from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import TestCase
from django.urls import reverse

from community.forms import TrailNoteForm
from community.models import TrailNote, Bookmark
from trips.models import Trip

User = get_user_model()



class TrailNoteFormTests(TestCase):

    def test_form_rejects_short_body(self):

        form = TrailNoteForm(data={'body': 'hi'})
        self.assertFalse(form.is_valid())
        self.assertIn('body', form.errors)

    def test_form_accepts_valid_body(self):

        form = TrailNoteForm(data={'body': 'This trail was spectacular, highly recommend.'})
        self.assertTrue(form.is_valid())



class TrailNoteModeratorTests(TestCase):

    def setUp(self):

        self.owner = User.objects.create_user(username='owner', password='pass')
        self.author = User.objects.create_user(username='author', password='pass')
        self.moderator = User.objects.create_user(username='mod', password='pass')

        mod_group, _ = Group.objects.get_or_create(name='Moderator')
        perm = Permission.objects.get(codename='can_moderate_trail_notes')
        mod_group.permissions.add(perm)
        self.moderator.groups.add(mod_group)

        self.trip = Trip.objects.create(
            owner = self.owner,
            title = 'Test Trip',
            description = '...',
            start_date = date.today(),
            end_date = date.today() + timedelta(days=1),
        )

        self.note = TrailNote.objects.create(
            trip = self.trip,
            author = self.author,
            body = 'Original note body, long enough to pass validation.',
        )

    def test_moderator_can_delete_any_note(self):

        self.client.login(username='mod', password='pass')
        response = self.client.post(
            reverse('community:note_delete', kwargs={'pk': self.note.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(TrailNote.objects.filter(pk=self.note.pk).exists())

    def test_random_user_cannot_delete_others_note(self):

        other = User.objects.create_user(username='other', password='pass')
        self.client.login(username='other', password='pass')
        response = self.client.get(
            reverse('community:note_delete', kwargs={'pk': self.note.pk})
        )

        self.assertEqual(response.status_code, 404)



class BookmarkToggleTests(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(username='rider', password='pass')
        self.trip = Trip.objects.create(
            owner=self.user,
            title='Trip',
            description='...',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
        )

    def test_toggle_creates_bookmark(self):

        self.client.login(username='rider', password='pass')
        self.client.post(
            reverse('trips:bookmark_toggle', kwargs={'slug': self.trip.slug})
        )

        self.assertTrue(
            Bookmark.objects.filter(user=self.user, trip=self.trip).exists()
        )

    def test_toggle_removes_bookmark(self):

        Bookmark.objects.create(user=self.user, trip=self.trip)
        self.client.login(username='rider', password='pass')
        self.client.post(
            reverse('trips:bookmark_toggle', kwargs={'slug': self.trip.slug})
        )

        self.assertFalse(
            Bookmark.objects.filter(user=self.user, trip=self.trip).exists()
        )