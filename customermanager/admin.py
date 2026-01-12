from django.contrib import admin
from .models import Customer


class AdminCustomer(admin.ModelAdmin):
    pass


admin.site.register(Customer, AdminCustomer)