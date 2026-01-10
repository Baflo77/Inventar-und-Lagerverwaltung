from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    # Frontend/API sendet nur "name"
    name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    # Optional: schöner Output für Swagger/Frontend
    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Customer
        fields = "__all__"  # behält alle echten Model-Felder (inkl. street/zip_code/...)
        # first_name/last_name sollen nicht direkt beschrieben werden (weil wir name nutzen)
        read_only_fields = ["first_name", "last_name"]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    def create(self, validated_data):
        # name kommt nicht aus dem Model, daher extra behandeln
        name_value = validated_data.pop("name", "")
        customer = Customer(**validated_data)
        if name_value is not None:
            customer.name = name_value  # nutzt deinen @name.setter -> first/last
        customer.save()
        return customer

    def update(self, instance, validated_data):
        name_value = validated_data.pop("name", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if name_value is not None:
            instance.name = name_value

        instance.save()
        return instance
