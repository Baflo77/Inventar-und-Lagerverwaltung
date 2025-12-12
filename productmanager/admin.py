from django.contrib import admin

from productmanager.models import Product


# Register your models here.
class AdminProduct(admin.ModelAdmin):
    pass

admin.site.register(Product, AdminProduct)