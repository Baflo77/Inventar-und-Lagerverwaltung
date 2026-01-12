from rest_framework import serializers
from django.db import models


class StockMovementSerializer(serializers.Serializer):
    product_name = serializers.ReadOnlyField(source='product.name')

    timestamp = models.DateTimeField(auto_now_add=True)
