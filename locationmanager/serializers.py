from rest_framework import serializers

class LocationSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=100)
