from django.db import models
from productmanager.models import Product
from purchaseordermanager.models import PurchaseOrder
from productsuppliermanager.models import ProductSupplier
from django.core.exceptions import ValidationError
from django.db.models import Max
from django.db import transaction


class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    product_supplier = models.ForeignKey(ProductSupplier, on_delete=models.PROTECT, related_name="purchase_order_items",)
    line_no = models.PositiveIntegerField() #null true, weil alte Daten keine line_no haben
    quantity = models.PositiveIntegerField()
    received_quantity = models.PositiveIntegerField(default=0)

    def clean(self):

        if self.purchase_order and self.product_supplier:
            if self.purchase_order.supplier_id != self.product_supplier.supplier_id:
                raise ValidationError(
                    "Der gewählte ProductSupplier gehört nicht zum Lieferanten dieser PurchaseOrder."
                )

    def save(self, *args, **kwargs):
        if not self.line_no:
            with transaction.atomic():
                max_no = (
                    PurchaseOrderItem.objects
                    .select_for_update()
                    .filter(purchase_order=self.purchase_order)
                    .aggregate(m=Max("line_no"))
                    ["m"]
                ) or 0
                self.line_no = max_no + 1

        self.full_clean()
        return super().save(*args, **kwargs)

    @property
    def product(self):
        return self.product_supplier.product

    def __str__(self):
        return f"{self.product_supplier.product.name} x{self.quantity}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["purchase_order", "line_no"],
                name="uniq_po_line_no"
            )
        ]