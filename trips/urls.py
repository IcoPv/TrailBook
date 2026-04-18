from django.urls import path, include

from gallery.views import PhotoUploadView
from trips.views import TripListView, TripDetailView, TripCreateView, TripUpdateView, TripDeleteView
from waypoints.views import WaypointFormsetView, WaypointCreateView

app_name = 'trips'


trips_urlpatterns = [
    path('', TripDetailView.as_view(), name='trip_detail'),
    path('update_trip/', TripUpdateView.as_view(), name='update_trip'),
    path('delete_trip/', TripDeleteView.as_view(), name='delete_trip'),
    path('waypoints/add-single/', WaypointCreateView.as_view(), name='add_single_waypoint'),
    path('waypoints/add/', WaypointFormsetView.as_view(), name='add_waypoints'),
    path('photos/upload/', PhotoUploadView.as_view(), name='upload_photo')
]
urlpatterns = [
    path('', TripListView.as_view(), name='trips_list'),
    path('create_trip/', TripCreateView.as_view(), name='create_trip'),
    path('<slug:slug>/', include(trips_urlpatterns)),
]