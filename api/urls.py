from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import TripViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'trips', TripViewSet, basename='trip')
urlpatterns = [
    path('', include(router.urls))
]