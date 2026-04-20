
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from community.views import BookmarkListView
from trailbook.views import HomeView

"""
URL configuration for trailbook project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""


from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('trips/', include('trips.urls')),
    path('waypoints/', include('waypoints.urls')),
    path('photos/', include('gallery.urls')),
    path('notes/', include('community.urls')),
    path('bookmarks/', BookmarkListView.as_view(), name='bookmarks'),
    path('api/', include('api.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]


handler404 = 'trailbook.views.page_not_found'
handler500 = 'trailbook.views.server_error'