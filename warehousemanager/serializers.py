from rest_framework import serializers

from locationmanager.models import Location
from .models import Warehouse

class WarehouseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    name = serializers.CharField(max_length=200)
    short_code = serializers.CharField(max_length=30, allow_blank=True, required=False, allow_null=True)

    def validate_location(self, value):
        if value is None:
            return value
        if not Location.objects.filter(pk=value.pk).exists():
            raise serializers.ValidationError("Location existiert nicht.")
        return value

    def create(self, validated_data):
        location_object = validated_data.pop("location", None)
        if location_object is not None:
            validated_data["location_id"] = location_object.pk

        return Warehouse.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if "name" in validated_data:
            instance.name = validated_data["name"]

        elif "short_code" in validated_data:
            instance.short_code = validated_data["short_code"]

        elif "location" in validated_data:
            loc = validated_data["location"]  # Location-Objekt oder None
            instance.location_id = loc.pk if loc is not None else None

        instance.save()
        return instance