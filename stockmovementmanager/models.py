from django.db import models

class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('IN', 'Wareneingang'),
        ('OUT', 'Warenausgang'),
        ('MOVE', 'Umlagerung'),
    ]

    product = models.ForeignKey(
        'productmanager.Product',on_delete=models.PROTECT,related_name='movements'
    )

    quantity = models.PositiveIntegerField(default=1, verbose_name="Menge")

    movement_type = models.CharField(
        max_length=4,choices=MOVEMENT_TYPES,verbose_name="Bewegungsart"
    )
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Zeitstempel")


    class Meta:
        ordering = ['-timestamp']  # Sortiert die Liste automatisch: Neueste zuerst
        verbose_name = "Lagerbewegung"
        verbose_name_plural = "Lagerbewegungen"

    def __str__(self):
        # Formatierung: Datum schön lesbar machen
        date_str = self.timestamp.strftime('%d.%m.%Y %H:%M')
        return f"{date_str} | {self.get_movement_type_display()}: {self.quantity}x {self.product.product_name}"



"""" 
class Stock(models.Model):
   


    quantity = models.IntegerField(default=0, verbose_name="Bestand")

    class Meta:
        verbose_name = "Lagerbestand"
        verbose_name_plural = "Lagerbestände"

    def __str__(self):
        return f"{self.product.product_name}: {self.quantity} Stück"

"""