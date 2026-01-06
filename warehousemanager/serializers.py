from rest_framework import serializers

from locationmanager.serializers import LocationSerializer
from warehousemanager.models import Warehouse


class WarehouseSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    locations = LocationSerializer(many=True)

    def create(self, validated_data):
        warehouse = Warehouse.objects.create(**validated_data)

    def update(self, instance, validated_data):
        name = validated_data.get('name')
        locations = validated_data.get('locations')
