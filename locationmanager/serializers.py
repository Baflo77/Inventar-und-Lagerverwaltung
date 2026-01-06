from rest_framework import serializers

from locationmanager.models import Location


class LocationSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Location.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.address = validated_data.get('address')
