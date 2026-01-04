from django.db import models

import locationmanager
import productmanager
import warehousemanager
from locationmanager.models import Location
from warehousemanager.models import Warehouse
from productmanager.models import Product

# Create your models here.
class Stock(models.Model):
    quantity = models.PositiveIntegerField(default=0,verbose_name="Aktueller Bestand")
    quantity_on_order = models.PositiveIntegerField(default=0, verbose_name="Bestellte Menge (Einkauf)")
    threshold = models.PositiveIntegerField(default=0,verbose_name="Meldebestand (Mindestmenge)")
    status = models.BooleanField(default=False)

    warehouse = models.ForeignKey('warehousemanager.Warehouse', on_delete=models.CASCADE, related_name='stock_items')
    location = models.ForeignKey('locationmanager.Location', on_delete=models.CASCADE, related_name='Lagerplatz')
    product = models.ForeignKey('productmanager.Product', on_delete=models.CASCADE, related_name='stock_entries')

    class Meta:
        unique_together = ['product', 'location']
        verbose_name = "Lagerbestand"
        verbose_name_plural = "Lagerbestände"

    def ausbuchen(self, menge):
        if menge <= 0:
            raise ValueError( "Bitte gib eine gültige Menge größer als 0 ein")
        if self.quantity < menge:
            raise ValueError(f"Nicht genug Bestand! Nur {self.quantity} verfügbar.")

        self.quantity -= menge
        self.save()
        return self.quantity

    # Der Ampel-Status (Automatisch)
    @property
    def status(self):
        if self.quantity == 0:
            return "LEER"
        elif self.quantity <= self.threshold:
            return "KRITISCH"
        return "OK"

    def __str__(self):
        return f"{Produkt} - {self.product}, Standort - {self.location}, Anzahl - {self.quantity}, Mindestbestand - {self.threshold}, Status - {self.status}, Warenhaus: {self.warehouse}"

