from rest_framework import serializers
from warehousemanager.models import Warehouse
from .models import Location

class LocationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200)
    description = serializers.CharField(allow_blank=True, required=False, allow_null=True)
    street = serializers.CharField(max_length=200, allow_blank=True, required=False, allow_null=True)
    zip_code = serializers.CharField(max_length=20, allow_blank=True, required=False, allow_null=True)
    city = serializers.CharField(max_length=100, allow_blank=True, required=False, allow_null=True)
    country = serializers.CharField(max_length=100, allow_blank=True, required=False, allow_null=True,)
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False, allow_null=True)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False, allow_null=True)
    warehouse = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all())
    capacity = serializers.IntegerField(required=False, min_value=0)

    def validate_warehouse(self, value):
        if value is None:
            raise serializers.ValidationError("Warehouse ist erforderlich.")
        return value

    def create(self, validated_data):
        warehouse = validated_data.pop("warehouse")
        return Location.objects.create(warehouse=warehouse, **validated_data)

    def update(self, instance, validated_data):
        if "warehouse" in validated_data:
            instance.warehouse = validated_data["warehouse"]

        for field in [
            "name", "description", "street", "zip_code",
            "city", "country", "latitude", "longitude","capacity",
        ]:
            if field in validated_data:
                setattr(instance, field, validated_data[field])

        instance.save()
        return instance