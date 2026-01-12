from django.db import models
from locationmanager.models import Location
from productmanager.models import Product


class Stock(models.Model):
    quantity = models.PositiveIntegerField(default=0, verbose_name="Aktueller Bestand")
    threshold = models.PositiveIntegerField(default=0, verbose_name="Meldebestand (Mindestmenge)")
    location = models.ForeignKey('locationmanager.Location', on_delete=models.CASCADE, related_name='stocks')
    product = models.ForeignKey('productmanager.Product', on_delete=models.CASCADE, related_name='stock_entries')

    class Meta:
        unique_together = ['product', 'location']
        verbose_name = "Lagerbestand"
        verbose_name_plural = "Lagerbestände"

    def __str__(self):
        return f"{self.product} @ {self.location} ({self.quantity})"
