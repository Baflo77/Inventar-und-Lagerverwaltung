from rest_framework import serializers

class StockSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(max_value=10000)
    threshold = serializers.IntegerField(max_value=100)
    status =  serializers.BooleanField()
