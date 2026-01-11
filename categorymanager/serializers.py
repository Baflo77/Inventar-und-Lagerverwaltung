from rest_framework import serializers
from categorymanager.models import Category


class CategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    id = serializers.IntegerField(required=False)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance:Category, validated_data):
        instance.name = validated_data.get('name')
        instance.save()
        return instance
