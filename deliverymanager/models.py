from django.db import models
from ordermanager.models import Order


class Delivery(models.Model):
    order = models.ForeignKey(
        "ordermanager.Order",
        on_delete=models.CASCADE,
        related_name="deliveries",
    )

    delivery_date = models.DateField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"Delivery #{self.id} for Order #{self.order_id}"

    class Meta:
        ordering = ["-delivery_date"]