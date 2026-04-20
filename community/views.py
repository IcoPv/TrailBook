from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from community.forms import TrailNoteForm
from community.models import TrailNote, Bookmark
from trips.models import Trip



class TrailNoteCreateView(LoginRequiredMixin, CreateView):
    model = TrailNote
    form_class = TrailNoteForm
    http_method_names = ['post']

    def dispatch(self, request, *args, **kwargs):
        self.trip = get_object_or_404(Trip, slug=kwargs['slug'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.trip = self.trip
        form.instance.author = self.request.user
        messages.success(self.request, 'Trail note added.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Your note could not be saved. Please check the content.')
        return redirect('trips:trip_detail', slug=self.trip.slug)

    def get_success_url(self):
        return reverse_lazy('trips:trip_detail', kwargs={'slug': self.trip.slug})



class TrailNoteUpdateView(LoginRequiredMixin, UpdateView):
    model = TrailNote
    form_class = TrailNoteForm
    template_name = 'community/trail-note-form.html'
    context_object_name = 'note'

    def get_queryset(self):
        qs = TrailNote.objects.all()
        user = self.request.user
        if user.has_perm('community.can_moderate_trail_notes'):
            return qs
        return qs.filter(author=user)

    def form_valid(self, form):
        messages.success(self.request, 'Trail note updated.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('trips:trip_detail', kwargs={'slug': self.object.trip.slug})



class TrailNoteDeleteView(LoginRequiredMixin, DeleteView):
    model = TrailNote
    template_name = 'community/trail-note-confirm-delete.html'
    context_object_name = 'note'

    def get_queryset(self):
        qs = TrailNote.objects.all()
        user = self.request.user
        if user.has_perm('community.can_moderate_trail_notes'):
            return qs
        return qs.filter(author=user)

    def get_success_url(self):
        messages.success(self.request, 'Trail note deleted.')
        return reverse_lazy('trips:trip_detail', kwargs={'slug': self.object.trip.slug})



class BookmarkToggleView(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request, slug):
        trip = get_object_or_404(Trip, slug=slug)
        bookmark, created = Bookmark.objects.get_or_create(user=request.user, trip=trip)
        if not created:
            bookmark.delete()
            messages.info(request, f"Removed '{trip.title}' from your saved trips.")
        else:
            messages.success(request, f"Saved '{trip.title}' to your bookmarks.")
        return redirect('trips:trip_detail', slug=trip.slug)



class BookmarkListView(LoginRequiredMixin, ListView):
    model = Bookmark
    template_name = 'community/bookmark-list.html'
    context_object_name = 'bookmarks'
    paginate_by = 10

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user).select_related('trip', 'trip__owner')
