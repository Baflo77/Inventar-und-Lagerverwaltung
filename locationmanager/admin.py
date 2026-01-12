from django.contrib import admin

from locationmanager.models import Location


class AdminLocation(admin.ModelAdmin):
    pass

admin.site.register(Location, AdminLocation)
# Register your models here.
