from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.http import HttpResponseForbidden
from django.views.generic import UpdateView, DeleteView

from trips.models import Trip
from waypoints.forms import WaypointFormset, WaypointForm
from waypoints.models import Waypoint


class WaypointFormsetView(LoginRequiredMixin, View):

    template_name = 'waypoints/waypoint-formset.html'

    def get_trip(self):
        trip = get_object_or_404(Trip, slug=self.kwargs['slug'])

        if trip.owner != self.request.user:
            return None
        return trip

    def get(self, request, slug):
        trip = self.get_trip()

        if trip is None:
            return HttpResponseForbidden("You dont have permission to add waypoints to this trip!")

        formset = WaypointFormset(instance=trip)

        return render(request, self.template_name, {
            'formset': formset,
            'trip': trip,
        })

    def post(self, request, slug):
        trip = self.get_trip()

        if trip is None:
            return HttpResponseForbidden("You dont have permission to add waypoints to this trip!")

        formset = WaypointFormset(request.POST, instance=trip)

        if formset.is_valid():
            formset.save()
            messages.success(request, "Waypoints added successfully!")
            return redirect('trips:trip_detail', slug=trip.slug)
        return render(request, self.template_name, {
            'formset': formset,
            'trip': trip,
        })



class WaypointUpdateView(LoginRequiredMixin, UpdateView):
    model = Waypoint
    form_class = WaypointForm
    template_name = 'waypoints/waypoint-form.html'
    context_object_name = 'waypoint'

    def get_queryset(self):
        return Waypoint.objects.filter(trip__owner=self.request.user)

    def get_success_url(self):
        messages.success(self.request, "Waypoint updated successfully!")
        return reverse_lazy('trips:trip_detail', kwargs={'slug': self.object.trip.slug})



class WaypointDeleteView(LoginRequiredMixin, DeleteView):
    model = Waypoint
    template_name = 'waypoints/waypoint-confirm-delete.html'
    context_object_name = 'waypoint'

    def get_queryset(self):
        return Waypoint.objects.filter(trip__owner=self.request.user)

    def get_success_url(self):
        messages.success(self.request, "Waypoint deleted successfully!")
        return reverse_lazy('trips:trip_detail', kwargs={'slug': self.object.trip.slug})
