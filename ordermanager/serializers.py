''''
from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
'''''

from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'product_name', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    items_count = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'customer', 'customer_name', 'date', 'status', 'items_count', 'total_price']

    def get_customer_name(self, obj):
        return f"{obj.customer.firstname} {obj.customer.lastname}"

    def get_items_count(self, obj):
        return obj.items.count()

    def get_total_price(self, obj):
        return round(sum(item.get_subtotal() for item in obj.items.all()), 2)
