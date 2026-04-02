from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.contrib.auth import get_user_model, logout
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from rest_framework.reverse import reverse_lazy

from accounts.forms import RegistrationForm, ProfileForm
from accounts.models import Profile

User = get_user_model()


class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        rider_group, _ = Group.objects.get_or_create(name='Rider')
        self.object.groups.add(rider_group)
        return response


class ProfileDetailView(DetailView):
    model = User
    template_name = 'accounts/profile-detail.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/profile-update.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={'username': self.request.user.username})


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'accounts/profile-delete-confirmation.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        logout(self.request)
        return super().form_valid(form)

    