
from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    productname = serializers.CharField(source='product.name', read_only=True)
    ordernumber = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'ordernumber', 'product', 'productname', 'quantity', 'subtotal']

    def get_ordernumber(self, obj):
        return f"Order #{obj.order.id}"

    def get_subtotal(self, obj):
        return round(obj.quantity * obj.product.unitprice, 2)


class OrderSerializer(serializers.ModelSerializer):
    customername = serializers.SerializerMethodField()
    itemscount = serializers.SerializerMethodField()
    totalprice = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'customer', 'customername', 'date', 'status', 'itemscount', 'totalprice', 'items']

    def get_customername(self, obj):
        return f"{obj.customer.firstname} {obj.customer.lastname}"

    def get_itemscount(self, obj):
        return obj.items.count()

    def get_totalprice(self, obj):
        return round(sum(item.get_subtotal() for item in obj.items.all()), 2)

    def get_items(self, obj):
        items = obj.items.all()
        return [
            {
                'id': item.id,
                'productname': item.product.name,
                'quantity': item.quantity,
                'price': float(item.product.unitprice)
            }
            for item in items
        ]
