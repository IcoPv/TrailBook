from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q, Exists, OuterRef
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from community.models import Bookmark
from trips.forms import TripSearchForm, TripForm
from trips.models import Trip


class TripListView(ListView):

    model = Trip
    template_name = 'trips/trips-list.html'
    context_object_name = 'trips'
    paginate_by = 10

    def get_queryset(self):

        queryset = Trip.objects.select_related('owner').prefetch_related('tags')
        form = TripSearchForm(self.request.GET)

        user = self.request.user

        if user.is_authenticated:
            queryset = queryset.annotate(
                is_bookmarked=Exists(
                    Bookmark.objects.filter(user=user, trip=OuterRef('pk'))
                )
            )

        if form.is_valid():
            query = form.cleaned_data.get('query')
            difficulty = form.cleaned_data.get('difficulty')
            vehicle_type = form.cleaned_data.get('vehicle_type')

            if query:
                queryset = queryset.filter(
                    Q(title__icontains=query) | Q(description__icontains=query)
                )

            if difficulty:
                queryset = queryset.filter(difficulty=difficulty)

            if vehicle_type:
                queryset = queryset.filter(vehicle_type=vehicle_type)

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['search_form'] = TripSearchForm(self.request.GET)

        return context



class TripDetailView(DetailView):

    model = Trip
    template_name = 'trips/trip-detail.html'
    context_object_name = 'trip'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            from community.models import Bookmark
            context['is_bookmarked'] = Bookmark.objects.filter(user=user, trip=self.object).exists()

        else:
            context['is_bookmarked'] = False
        return context

class TripCreateView(LoginRequiredMixin, CreateView):

    model = Trip
    form_class = TripForm
    template_name = 'trips/trip-form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Trip created successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('trips:trip_detail', kwargs={'slug': self.object.slug})



class TripUpdateView(LoginRequiredMixin, UpdateView):

    model = Trip
    form_class = TripForm
    template_name = 'trips/trip-form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Trip.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Trip updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('trips:trip_detail', kwargs={'slug': self.object.slug})



class TripDeleteView(LoginRequiredMixin, DeleteView):

    model = Trip
    template_name = 'trips/trip-confirm-delete.html'
    success_url = reverse_lazy('trips:trips_list')

    def get_queryset(self):
        return Trip.objects.filter(owner=self.request.user)




class ToggleFeaturedView(LoginRequiredMixin, PermissionRequiredMixin, View):

    permission_required = 'trips.can_feature_trips'
    http_method_names = ['post']

    def post(self, request, slug):

        trip = get_object_or_404(Trip, slug=slug)
        trip.is_featured = not trip.is_featured
        trip.save(update_fields=['is_featured'])
        action = 'featured' if trip.is_featured else 'unfeatured'
        messages.success(request, f"Trip {action}.")
        return redirect('trips:trip_detail', slug=trip.slug)