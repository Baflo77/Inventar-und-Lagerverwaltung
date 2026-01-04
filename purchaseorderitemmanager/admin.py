from django.contrib import admin

from purchaseordermanager.models import PurchaseOrder
from .models import PurchaseOrderItem
# Register your models here.

class AdminPurchaseOrderItem(admin.ModelAdmin):
    pass
admin.site.register(PurchaseOrderItem, AdminPurchaseOrderItem)
