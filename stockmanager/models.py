from django.db import models

from locationmanager.models import Location
from warehousemanager.models import Warehouse
from productmanager.models import Product

# Create your models here.
class Stock(models.Model):
    quantity = models.PositiveIntegerField(default=0)
    threshold = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=False)

    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='warehouses')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='locations')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return f"Produkt: {self.product}, Standort: {self.location}, Anzahl: {self.quantity}, Mindestbestand: {self.threshold}, Status: {self.status}, Warenhaus: {self.warehouse}"
