from django.db import models
from productmanager.models import Product
from purchaseordermanager.models import PurchaseOrder
from productsuppliermanager.models import ProductSupplier



class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    product_supplier = models.ForeignKey(ProductSupplier, on_delete=models.PROTECT, related_name="purchase_order_items",)
    #nachher entfernen!!!
    quantity = models.PositiveIntegerField()
    received_quantity = models.PositiveIntegerField(default=0)

    def clean(self):

        if self.purchase_order and self.product_supplier:
            if self.purchase_order.supplier_id != self.product_supplier.supplier_id:
                raise ValidationError(
                    "Der gewählte ProductSupplier gehört nicht zum Lieferanten dieser PurchaseOrder."
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} {self.quantity}"