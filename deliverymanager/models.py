from django.db import models


class Delivery(models.Model):
    STATUS_OPEN = "open"
    STATUS_SHIPPED = "shipped"
    STATUS_DELIVERED = "delivered"

    STATUS_CHOICES = [
        (STATUS_OPEN, "Open"),
        (STATUS_SHIPPED, "Shipped"),
        (STATUS_DELIVERED, "Delivered"),
    ]

    order = models.ForeignKey(
        "ordermanager.Order",
        on_delete=models.CASCADE,
        related_name="deliveries",
    )

    delivery_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_OPEN,
    )

    def __str__(self):
        return f"Delivery #{self.id} for Order #{self.order_id}"

    class Meta:
        ordering = ["-delivery_date"]