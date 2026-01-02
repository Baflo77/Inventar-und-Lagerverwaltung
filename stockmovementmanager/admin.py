from django.contrib import admin

from stockmovementmanager.models import StockMovement


# Register your models here.
class AdminMovement(admin.ModelAdmin):
    pass

admin.site.register(StockMovement, AdminMovement)