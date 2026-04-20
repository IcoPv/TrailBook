from rest_framework import serializers

from trips.models import Tag, Trip
from waypoints.models import Waypoint


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']



class WaypointSerializer(serializers.ModelSerializer):

    class Meta:
        model = Waypoint
        fields = ['id', 'name', 'latitude', 'longitude', 'elevation', 'order']




class TripListSerializer(serializers.ModelSerializer):

    owner = serializers.StringRelatedField()
    tags = TagSerializer(many=True, read_only=True)
    waypoint_count = serializers.IntegerField(source='waypoints.count', read_only=True)

    class Meta:
        model = Trip
        fields = [
            'id', 'title', 'slug', 'owner', 'difficulty',
            'vehicle_type', 'tags', 'start_date', 'end_date',
            'waypoint_count', 'created_at',
        ]



class TripDetailSerializer(TripListSerializer):

    waypoints = WaypointSerializer(many=True, read_only=True)

    class Meta(TripListSerializer.Meta):
        fields = TripListSerializer.Meta.fields + ['description', 'waypoints']