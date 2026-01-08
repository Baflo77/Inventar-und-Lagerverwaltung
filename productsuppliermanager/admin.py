from django.contrib import admin
from .models import ProductSupplier

# Register your models here.

@admin.register(ProductSupplier)
class ProductSupplierAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "supplier", "purchase_price", "delivery_time_days", "min_order_quantity")
    list_filter = ("supplier",)
    search_fields = ("product__name", "supplier__name")

