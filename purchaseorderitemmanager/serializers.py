from rest_framework import serializers
from .models import PurchaseOrderItem

class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderItem
        fields = "__all__"
        extra_kwargs = {
            "received_quantity": {"required": False},
        }