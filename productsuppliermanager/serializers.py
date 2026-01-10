from rest_framework import serializers
from .models import ProductSupplier

class ProductSupplierSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_sku = serializers.CharField(source="product.sku", read_only=True)
    supplier_name = serializers.CharField(source="supplier.name", read_only=True)
    class Meta:
        model = ProductSupplier
        fields = "__all__"
