from django.contrib import admin
from .models import PurchaseOrder
# Register your models here.
class AdminPurchaseOrder(admin.ModelAdmin):
    pass

admin.site.register(PurchaseOrder, AdminPurchaseOrder)