from django.contrib import admin

from warehousemanager.models import Warehouse


class AdminWarehouse(admin.ModelAdmin):
    pass

admin.site.register(Warehouse, AdminWarehouse)
# Register your models here.
