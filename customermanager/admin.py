from django.contrib import admin

from customermanager.models import Customer

# Register your models here.
class AdminCustomer(admin.ModelAdmin):
    pass

admin.site.register(Customer, AdminCustomer)