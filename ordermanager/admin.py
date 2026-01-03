from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'created_at', 'status']
    list_filter = ['status', 'created_at']
    search_fields = ['customer__firstname', 'customer__lastname']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity']
    search_fields = ['order__id', 'product__name']
