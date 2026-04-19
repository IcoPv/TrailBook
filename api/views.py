from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from api.serializers import TripDetailSerializer, TripListSerializer
from trips.models import Trip

class TripViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Trip.objects.select_related('owner').prefetch_related('tags', 'waypoints')
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['difficulty', 'vehicle_type']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TripDetailSerializer
        return TripListSerializer
