from django.db import models

class Location(models.Model):
    warehouse = models.ForeignKey("warehousemanager.Warehouse",on_delete=models.CASCADE,related_name="locations",)

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    street = models.CharField(max_length=200, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True, default="Deutschland")

    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name