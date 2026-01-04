from rest_framework import serializers
from .models import PurchaseOrder

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ["id", "supplier", "status", "created_at"]
        read_only_fields = ["id", "created_at"]

