from django.db import models

class Warehouse(models.Model):
    name = models.CharField(max_length=200)
    short_code = models.CharField(max_length=30, blank=True, null=True)

    # Damit SQL "location_id" passt:
    location = models.ForeignKey("locationmanager.Location", null=True, blank=True, on_delete=models.SET_NULL, related_name="primary_for_warehouses",)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.name}" + (f" ({self.short_code})" if self.short_code else "")