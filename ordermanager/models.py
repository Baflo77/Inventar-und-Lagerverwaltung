
# Create your models here.
from django.db import models
from customermanager.models import Customer
from productmanager.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("IN_PROCESS", "In process"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="OPEN")

    def __str__(self):
        return f"Order {self.id} ({self.customer})"


class OrderPosition(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="positions")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product} (Order {self.order_id})"
