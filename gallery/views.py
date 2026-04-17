from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView

from gallery.forms import PhotoUploadForm
from gallery.models import Photo
from trips.models import Trip


class PhotoUploadView(LoginRequiredMixin, CreateView):

    model = Photo
    form_class = PhotoUploadForm
    template_name = 'gallery/photo-upload.html'

    def dispatch(self, request, *args, **kwargs):
        self.trip = get_object_or_404(Trip, slug=kwargs['slug'])
        if self.trip.owner != request.user:
            return HttpResponseForbidden("You don't have permission to upload photos to this trip!")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['trip'] = self.trip
        return kwargs

    def form_valid(self, form):
        form.instance.trip = self.trip
        form.instance.uploaded_by = self.request.user
        messages.success(self.request, "Photo uploaded successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trip'] = self.trip
        return context

    def get_success_url(self):
        return reverse_lazy('trips:trip_detail', kwargs={'slug': self.trip.slug})



class PhotoDeleteView(LoginRequiredMixin, DeleteView):

    model = Photo
    template_name = 'gallery/photo-confirm-delete.html'
    context_object_name = 'photo'

    def get_queryset(self):
        return Photo.objects.filter(trip__owner=self.request.user)

    def get_success_url(self):
        messages.success(self.request, "Photo deleted successfully!")
        return reverse_lazy('trips:trip_detail', kwargs={'slug': self.object.trip.slug})