from django.contrib import admin
from .models import Order, OrderItem

# Inline für Items direkt in Order bearbeiten
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'date', 'status']
    list_filter = ['status', 'date']
    search_fields = ['customer__firstname', 'customer__lastname']
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity']
    search_fields = ['order__id', 'product__name']
