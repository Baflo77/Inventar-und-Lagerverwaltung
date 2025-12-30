from django.contrib import admin

from customermanager.models import Customer

# Register your models here.
class AdminCustomer(admin.ModelAdmin):
    list_display = ["first_name", "last_name"]
    '''
    fieldsets = [
        ("Basisdaten",{"fields":["user__first_name","last_name","email"]}),
        ("Kundendetails", {"fields":["salutation", "phone"]})
    ]
    '''


admin.site.register(Customer, AdminCustomer)