from django.contrib import admin

from categorymanager.models import Category


# Register your models here.
class AdminCategory(admin.ModelAdmin):
    pass

admin.site.register(Category, AdminCategory)