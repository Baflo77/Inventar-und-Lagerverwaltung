from django.db import models

class Location(models.Model):
    # Basis-Informationen
    name = models.CharField(max_length=255, verbose_name="Name des Standorts")
    description = models.TextField(blank=True, null=True, verbose_name="Beschreibung")
    warehouse = models.ForeignKey('warehousemanager.Warehouse', on_delete=models.CASCADE,related_name='locations',null=True, blank=True)
    capacity = models.PositiveIntegerField(default=0)
    # Adresse
    street = models.CharField(max_length=255, verbose_name="Straße & Hausnummer")
    city = models.CharField(max_length=100, verbose_name="Stadt")
    zip_code = models.CharField(max_length=20, verbose_name="PLZ")
    country = models.CharField(max_length=100, default="Deutschland", verbose_name="Land")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    class Meta:
        verbose_name = "Standort"
        verbose_name_plural = "Standorte"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.city})"

