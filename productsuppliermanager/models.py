from django.db import models
from django.core.validators import MinValueValidator #validator, verhindert negative Preise
# Create your models here.

class ProductSupplier(models.Model):


    # Verknüpfung zum Product-Model

    # auf ein Produkt zeigen n:1
    product = models.ForeignKey(
        "productmanager.Product",
        on_delete=models.CASCADE,            # Wenn das Produkt gelöscht wird, wird der Eintrag mitgelöscht
        related_name="supplier_links"        # Zugriff: product.supplier_links.all()
    )

    # Verknüpfung zum Supplier-Model
    supplier = models.ForeignKey(
        "suppliermanager.Supplier",          # Ziel-Model
        on_delete=models.CASCADE,            # Wenn der Lieferant gelöscht wird, wird der Eintrag mitgelöscht
        related_name="product_links"
    )

    # Einkaufspreis des Produkts bei diesem Lieferanten
    # DecimalField für Geldbeträge
    purchase_price = models.DecimalField(
        max_digits=10,                       # Gesamtanzahl der Ziffern
        decimal_places=2,                    # 2 Nachkommastellen
        validators=[MinValueValidator(0)],   # keine neg Preise
        null=True,                           # Feld darf in Datenbank leer sein
        blank=True                           # Feld darf im Formular leer sein
    )

    # Lieferzeit in Tagen für diesen Lieferanten
    delivery_time_days = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    # Mindestbestellmenge bei diesem Lieferanten
    min_order_quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        null=True,
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product", "supplier"],
                name="unique_product_supplier"
            )
        ]


    def __str__(self):
        return f"{self.product} ↔ {self.supplier}"