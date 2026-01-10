from django.db import models

class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('IN', 'Wareneingang'),
        ('OUT', 'Warenausgang'),
        ('MOVE', 'Umlagerung'),
    ]

    product = models.ForeignKey('productmanager.Product',on_delete=models.PROTECT,related_name='movements')
    source_location = models.ForeignKey('locationmanager.Location', on_delete=models.SET_NULL, null=True, blank=True,related_name='movements_from', verbose_name="Von Lagerort")
    destination_location = models.ForeignKey('locationmanager.Location', on_delete=models.SET_NULL, null=True, blank=True,related_name='movements_to', verbose_name="Nach Lagerort")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Menge")
    movement_type = models.CharField(max_length=4,choices=MOVEMENT_TYPES,verbose_name="Bewegungsart")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Zeitstempel")
    note = models.TextField(blank=True, null=True, verbose_name="Bemerkung")


    class Meta:
        ordering = ['-timestamp']  # Sortiert die Liste automatisch: Neueste zuerst
        verbose_name = "Lagerbewegung"
        verbose_name_plural = "Lagerbewegungen"

    def __str__(self):
        date_str = self.timestamp.strftime('%d.%m.%Y %H:%M')


        loc_info = ""
        if self.source_location and self.destination_location:
            loc_info = f"({self.source_location} -> {self.destination_location})"
        elif self.source_location:
            loc_info = f"(von {self.source_location})"
        elif self.destination_location:
            loc_info = f"(nach {self.destination_location})"

        return f"{date_str} | {self.get_movement_type_display()}: {self.quantity}x {self.product} {loc_info}"



