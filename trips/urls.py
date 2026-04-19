from django.urls import path, include

from community.views import TrailNoteCreateView, BookmarkToggleView
from gallery.views import PhotoUploadView
from trips.views import TripListView, TripDetailView, TripCreateView, TripUpdateView, TripDeleteView, ToggleFeaturedView
from waypoints.views import WaypointFormsetView, WaypointCreateView

app_name = 'trips'


trips_urlpatterns = [
    path('', TripDetailView.as_view(), name='trip_detail'),
    path('update_trip/', TripUpdateView.as_view(), name='update_trip'),
    path('delete_trip/', TripDeleteView.as_view(), name='delete_trip'),
    path('waypoints/add-single/', WaypointCreateView.as_view(), name='add_single_waypoint'),
    path('waypoints/add/', WaypointFormsetView.as_view(), name='add_waypoints'),
    path('photos/upload/', PhotoUploadView.as_view(), name='upload_photo'),
    path('notes/add/', TrailNoteCreateView.as_view(), name='add_note'),
    path('bookmark/', BookmarkToggleView.as_view(), name='bookmark_toggle'),
    path('toggle-featured/', ToggleFeaturedView.as_view(), name='toggle_featured'),
]
urlpatterns = [
    path('', TripListView.as_view(), name='trips_list'),
    path('create_trip/', TripCreateView.as_view(), name='create_trip'),
    path('<slug:slug>/', include(trips_urlpatterns)),
]