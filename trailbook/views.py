from django.shortcuts import render
from django.views.generic import TemplateView

from trips.models import Trip


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_trips'] = Trip.objects.filter(
            is_featured=True
        ).select_related('owner').prefetch_related('tags')[:6]
        return context



def page_not_found(request, exception):
    return render(request, '404.html', status=404)

def server_error(request):
    return render(request, '500.html', status=500)

