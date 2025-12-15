from django.db import models

import locationmanager
import productmanager
import warehousemanager
from locationmanager.models import Location
from warehousemanager.models import Warehouse
from productmanager.models import Product

# Create your models here.
class Stock(models.Model):
    quantity = models.PositiveIntegerField(default=0)
    threshold = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=False)

    warehouse = models.ForeignKey('warehousemanager.Warehouse', on_delete=models.CASCADE, related_name='stock_items')
    location = models.ForeignKey('locationmanager.Location', on_delete=models.CASCADE, related_name='stock_items')
    product = models.ForeignKey('productmanager.Product', on_delete=models.CASCADE, related_name='stock_entries')

"""" "
    def __str__(self):
        return f"Produkt: {self.product}, Standort: {self.location}, Anzahl: {self.quantity}, Mindestbestand: {self.threshold}, Status: {self.status}, Warenhaus: {self.warehouse}"

"""