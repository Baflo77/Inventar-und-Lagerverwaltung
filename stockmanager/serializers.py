from rest_framework import serializers
from .models import Stock

class StockSerializer(serializers.Serializer):

    status = status = serializers.ReadOnlyField()
    product_name = serializers.CharField(source='product.name', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)

    quantity = serializers.IntegerField(max_value=10000)
    threshold = serializers.IntegerField(max_value=100)

    def create(self, validated_data):
        return Stock.objects.create(**validated_data)

    def update(self, instance:Stock, validated_data):
        instance.location_name = validated_data.get('location_name')
        instance.warehouse_name = validated_data.get('warehouse_name')
        instance.quantity = validated_data.get('quantity')

    class Meta:
        model = Stock
        #Listen  aller Felder, die die API rausgeben soll
        fields = [
            'id',
            'product', 'product_name',
            'location', 'location_name',
            'warehouse', 'warehouse_name',
            'quantity',
            'quantity_on_order',
            'threshold',
            'status'
        ]