from django.contrib import admin

from deliverymanager.models import Delivery


# Register your models here.
class AdminDelivery(admin.ModelAdmin):
    pass

admin.site.register(Delivery, AdminDelivery)