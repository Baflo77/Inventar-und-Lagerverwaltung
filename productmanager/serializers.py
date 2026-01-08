from rest_framework import serializers
from categorymanager.models import Category
from productmanager.models import Product
from suppliermanager.models import Supplier

class ProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    sku = serializers.CharField(max_length=100)
    description = serializers.CharField()
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    id = serializers.IntegerField(required=False)

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance:Product, validated_data):
        instance.name = validated_data.get('name')
        instance.sku = validated_data.get('sku')
        instance.description = validated_data.get('description')
        instance.supplier = validated_data.get('supplier')
        instance.category = validated_data.get('category')
        instance.save()
        return instance
