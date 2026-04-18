from django.urls import path, include

from waypoints.views import WaypointUpdateView, WaypointDeleteView



app_name = 'waypoints'
urlpatterns = [
    path('<int:pk>/', include(
        [
            path('edit/', WaypointUpdateView.as_view(), name='waypoint_edit'),
            path('delete/', WaypointDeleteView.as_view(), name='waypoint_delete'),
        ]
    ))
]