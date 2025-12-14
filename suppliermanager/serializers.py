from rest_framework import serializers

from suppliermanager.models import Supplier


class SupplierSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    contact_person =serializers.CharField(max_length=30)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=15)
    postal_code = serializers.IntegerField()
    city = serializers.CharField(max_length=25)
    street = serializers.CharField(max_length=25)
    house_number = serializers.IntegerField()
    id = serializers.IntegerField(required=False)

    def create(self, validated_data):
        return Supplier.objects.create(**validated_data)

    def update(self, instance:Supplier, validated_data):
        instance.name = validated_data.get('name')
        instance.contact_person = validated_data.get('contact_person')
        instance.email = validated_data.get('email')
        instance.phone = validated_data.get('phone')
        instance.postal_code = validated_data.get('postal_code')
        instance.city = validated_data.get('city')
        instance.street = validated_data.get('street')
        instance.house_number = validated_data.get('house_number')
        instance.save()
        return instance