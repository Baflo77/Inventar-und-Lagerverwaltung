from django.db import models
from locationmanager.models import Location
from productmanager.models import Product


class Stock(models.Model):
    quantity = models.PositiveIntegerField(default=0, verbose_name="Aktueller Bestand")
    quantity_on_order = models.PositiveIntegerField(default=0, verbose_name="Bestellte Menge (Einkauf)")
    threshold = models.PositiveIntegerField(default=0, verbose_name="Meldebestand (Mindestmenge)")

    location = models.ForeignKey('locationmanager.Location', on_delete=models.CASCADE, related_name='stocks')
    product = models.ForeignKey('productmanager.Product', on_delete=models.CASCADE, related_name='stock_entries')

    class Meta:
        unique_together = ['product', 'location']
        verbose_name = "Lagerbestand"
        verbose_name_plural = "Lagerbestände"

    def ausbuchen(self, menge):
        if menge <= 0:
            raise ValueError("Bitte gib eine gültige Menge größer als 0 ein")
        if self.quantity < menge:
            raise ValueError(f"Nicht genug Bestand! Nur {self.quantity} verfügbar.")

        self.quantity -= menge
        self.save()
        return self.quantity

    @property
    def status(self):
        if self.quantity == 0:
            return "LEER"
        elif self.quantity <= self.threshold:
            return "KRITISCH"
        return "OK"

    def __str__(self):
        return f"{self.product} @ {self.location} ({self.quantity})"



class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('IN', 'Wareneingang'),
        ('OUT', 'Warenausgang'),
        ('MOVE', 'Umlagerung'),
    ]

    product = models.ForeignKey('productmanager.Product',on_delete=models.PROTECT, related_name='sm_movements')
    source_location = models.ForeignKey('locationmanager.Location',on_delete=models.SET_NULL,null=True,blank=True,related_name='sm_movements_from',verbose_name="Von Lagerort")
    destination_location = models.ForeignKey('locationmanager.Location',on_delete=models.SET_NULL,null=True,blank=True,related_name='sm_movements_to',verbose_name="Nach Lagerort")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Menge")
    movement_type = models.CharField(max_length=4,choices=MOVEMENT_TYPES,verbose_name="Bewegungsart")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Zeitstempel")

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Lagerbewegung"
        verbose_name_plural = "Lagerbewegungen"

    def __str__(self):
        return f"{self.get_movement_type_display()}: {self.quantity}x {self.product}"