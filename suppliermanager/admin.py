from django.contrib import admin

from suppliermanager.models import Supplier


# Register your models here.
class AdminSupplier(admin.ModelAdmin):
    pass

admin.site.register(Supplier, AdminSupplier)