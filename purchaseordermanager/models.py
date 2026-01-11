from django.db import models
from suppliermanager.models import Supplier
# Create your models here.

class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ("open", "Offen"),
        ("ordered", "Bestellt"),
        ("delivered", "Geliefert"),
        ("canceled", "Storniert"),
    ]

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="ordered")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Purchase Order #{self.pk}, Status: {self.status}, Bestellt am: {self.created_at}"