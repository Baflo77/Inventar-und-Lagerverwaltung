from django.db import models
from warehousemanager.models import Warehouse
# Create your models here.
class Location(models.Model):
    address = models.CharField(max_length=100)

    ##warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='warehouses')

    warehouse = models.ForeignKey( 'warehousemanager.Warehouse',on_delete=models.CASCADE,related_name='locations'
    )


    def __str__(self):
        return f"Addresse: {self.address}, Warenhaus: {self.warehouse}"

