from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from customermanager.models import Customer
from productmanager.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Ausstehend"),
        ("CONFIRMED", "Bestätigt"),
        ("SHIPPED", "Versendet"),
        ("DELIVERED", "Geliefert"),
        ("CANCELLED", "Storniert"),
    ]

    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order #{self.id} - {self.customer.firstname} {self.customer.lastname}"

    def get_total_price(self):
        """Berechnet Gesamtpreis aller Items"""
        return sum(item.get_subtotal() for item in self.items.all())

    def get_total_quantity(self):
        """Berechnet Gesamtmenge aller Items"""
        return sum(item.quantity for item in self.items.all())

    def can_ship(self):
        """Validierung: Order nur versendbar wenn CONFIRMED"""
        return self.status == "CONFIRMED"

    def ship(self):
        """Status zu SHIPPED ändern"""
        if not self.can_ship():
            raise ValidationError(f"Order {self.id} kann nicht versendet werden (Status: {self.status})")
        self.status = "SHIPPED"
        self.save()


class OrderItem(models.Model):
    """Einzelne Positionen einer Bestellung (1:N zu Order)"""
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT  # Produkt darf nicht gelöscht werden wenn noch Bestellungen existieren
    )
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ('order', 'product')  # Kein Duplikat: Selbes Produkt mehrmals in Order
        verbose_name_plural = "Order Items"

    def clean(self):
        """Validierung: Menge darf nicht negativ sein"""
        if self.quantity <= 0:
            raise ValidationError("Bestellmenge muss größer als 0 sein!")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def get_subtotal(self):
        """Berechnet Zwischensumme (quantity × unit_price)"""
        return self.quantity * self.product.unit_price

    def __str__(self):
        return f"{self.quantity}x {self.product.name} (Order #{self.order_id})"
