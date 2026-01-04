from django.db import models


class DeliveryItem(models.Model):
    delivery = models.ForeignKey(
        "deliverymanager.Delivery",
        on_delete=models.CASCADE,
        related_name="items",
    )

    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"DeliveryItem #{self.id}: {self.quantity} x {self.description} (Delivery #{self.delivery_id})"



