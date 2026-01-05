from rest_framework import serializers

from locationmanager.serializers import LocationSerializer


class WarehouseSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    locations = LocationSerializer(many=True)
