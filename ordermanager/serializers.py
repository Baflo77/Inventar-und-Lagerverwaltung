from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    productname = serializers.CharField(source='product.name', read_only=True)
    ordernumber = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'productname', 'quantity', 'ordernumber', 'subtotal']

    def get_ordernumber(self, obj):
        return f"Order #{obj.order.id}"

    def get_subtotal(self, obj):
        return obj.get_subtotal()


class OrderSerializer(serializers.ModelSerializer):
    customername = serializers.SerializerMethodField()
    itemscount = serializers.SerializerMethodField()
    totalprice = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'customer', 'customername', 'date', 'status', 'itemscount', 'totalprice', 'items']

    def get_customername(self, obj):
        customer = obj.customer
        # Sucht nach firstname/lastname oder first_name/last_name
        first = getattr(customer, 'firstname', getattr(customer, 'first_name', ''))
        last = getattr(customer, 'lastname', getattr(customer, 'last_name', ''))

        full_name = f"{first} {last}".strip()
        return full_name if full_name else f"Customer #{customer.id}"

    def get_itemscount(self, obj):
        return obj.items.count()

    def get_totalprice(self, obj):
        return round(obj.get_total_price(), 2)

    def get_items(self, obj):
        items = obj.items.select_related('product').all()
        return [
            {
                'id': item.id,
                'productname': item.product.name,
                'quantity': item.quantity,
                # FIX: Hier holen wir auch 'unitprice' (ohne Unterstrich) oder 'price'
                'price': float(getattr(item.product, 'unitprice', getattr(item.product, 'price', 0)))
            }
            for item in items
        ]
