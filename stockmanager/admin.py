from django.contrib import admin
from stockmanager.models import Stock


class AdminStock(admin.ModelAdmin):
    pass


admin.site.register(Stock, AdminStock)
