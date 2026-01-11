from django.db import models
from django.core.exceptions import ValidationError
from customermanager.models import Customer
from productmanager.models import Product
from django.apps import apps
from django.db import transaction

class Order(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Ausstehend"), ("CONFIRMED", "Bestätigt"),
        ("SHIPPED", "Versendet"), ("DELIVERED", "Geliefert"), ("CANCELLED", "Storniert")
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order #{self.id} - {self.customer.firstname} {self.customer.lastname}"

    def get_total_price(self):
        return sum(item.get_subtotal() for item in self.items.all())

    def get_total_quantity(self):
        return sum(item.quantity for item in self.items.all())

    def can_ship(self):
        return self.status == "CONFIRMED"

    def ship(self):
        if not self.can_ship():
            raise ValidationError(f"Order {self.id} kann nicht versendet werden (Status: {self.status})")
        self.status = "SHIPPED"
        self.save()

    @transaction.atomic
    def create_delivery_from_orderitems(self, delivery_date, status="open"):
        """
        Erstellt eine Delivery zu dieser Order und kopiert OrderItems -> DeliveryItems.
        Nutzt apps.get_model, um keine Circular Imports zu bauen.
        """
        Delivery = apps.get_model("deliverymanager", "Delivery")
        DeliveryItem = apps.get_model("deliveryitem", "DeliveryItem")

        delivery = Delivery.objects.create(
            order=self,
            delivery_date=delivery_date,
            status=status,
        )

        for oi in self.items.select_related("product").all():
            # Variante A (BEST): DeliveryItem hat ein product-FK
            if hasattr(DeliveryItem, "product_id"):
                DeliveryItem.objects.create(
                    delivery=delivery,
                    product=oi.product,
                    quantity=oi.quantity,
                    description=oi.product.name if hasattr(DeliveryItem, "description") else None,
                )
            else:
                # Variante B: DeliveryItem hat nur description + quantity
                DeliveryItem.objects.create(
                    delivery=delivery,
                    description=oi.product.name,
                    quantity=oi.quantity,
                )

        return delivery

    def clean(self):
        super().clean()
        if self.status == 'SHIPPED' and not self.items.exists():
            raise ValidationError("Order kann nicht versendet werden ohne Items!")

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ('order', 'product')
        verbose_name_plural = "Order Items"

    def clean(self):
        if self.quantity <= 0:
            raise ValidationError("Bestellmenge muss größer als 0 sein!")

    def save(self, *args, **kwargs):
        if hasattr(self.product, 'stock') and self.product.stock < self.quantity:
            raise ValidationError(f"Lagerbestand unzureichend: {self.product.stock} < {self.quantity}")
        self.full_clean()
        super().save(*args, **kwargs)

    def get_subtotal(self):
        return self.quantity * self.product.unit_price

    def __str__(self):
        return f"{self.quantity}x {self.product.name} (Order #{self.order_id})"
