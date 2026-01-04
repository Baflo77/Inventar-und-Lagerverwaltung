from rest_framework import serializers

class WarehouseSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
