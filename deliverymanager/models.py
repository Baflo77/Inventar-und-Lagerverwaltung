'''
from django.db import models



# Create your models here.
# deliverymanager/models.py

# Wenn eure Order-App z.B. "ordermanager" heißt:
from ordermanager.models import Order

class Delivery(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="deliveries"
    )
    delivery_date = models.DateField()
    status = models.BooleanField()  # oder besser CharField mit Choices

    def __str__(self):
        return f"Delivery {self.id} for order {self.order_id}"
'''
