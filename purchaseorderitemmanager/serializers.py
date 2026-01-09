from rest_framework import serializers
from .models import PurchaseOrderItem

class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderItem
        fields = ["id", "purchase_order", "product", "quantity", "received_quantity"]
        read_only_fields = ["received_quantity"]