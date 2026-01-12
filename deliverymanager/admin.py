from django.contrib import admin
from .models import Delivery
from deliveryitem.models import DeliveryItem

class DeliveryItemInline(admin.TabularInline):
    model = DeliveryItem
    extra = 1

class AdminDelivery(admin.ModelAdmin):
    pass

admin.site.register(Delivery, AdminDelivery)