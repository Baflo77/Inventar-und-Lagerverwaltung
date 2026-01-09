from django.db import models
from productmanager.models import Product
from purchaseordermanager.models import PurchaseOrder
# Create your models here.

class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    received_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} {self.quantity}"