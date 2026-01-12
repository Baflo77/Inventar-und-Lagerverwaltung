from django.contrib import admin
from productsuppliermanager.models import ProductSupplier

class AdminProductSupplier(admin.ModelAdmin):
    pass

admin.site.register(ProductSupplier, AdminProductSupplier)
