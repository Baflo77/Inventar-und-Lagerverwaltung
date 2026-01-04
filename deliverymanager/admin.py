from django.contrib import admin
from .models import Delivery
from deliveryitem.models import DeliveryItem


class DeliveryItemInline(admin.TabularInline):
    model = DeliveryItem
    extra = 1


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    inlines = [DeliveryItemInline]
    list_display = ("id", "order", "delivery_date", "status")
    list_filter = ("status",)