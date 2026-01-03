from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'date', 'status']
    list_filter = ['status', 'date']
    search_fields = ['customer__firstname', 'customer__lastname']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity']
    search_fields = ['order__id', 'product__name']
