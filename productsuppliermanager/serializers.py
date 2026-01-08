from rest_framework import serializers
from .models import ProductSupplier

class ProductSupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSupplier
        fields = "__all__"
