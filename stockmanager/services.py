from django.db import transaction
from django.core.exceptions import ValidationError
from stockmanager.models import Stock
from stockmovementmanager.models import StockMovement


def process_outgoing_goods(stock_id, quantity, user=None, notes=""):
    """
    Verarbeitet Warenausgang für einen spezifischen Lagerplatz (Stock ID).
    """
    with transaction.atomic():
        # 1. Lagerbestand holen und sperren (verhindert Race Conditions)
        stock = Stock.objects.select_for_update().get(pk=stock_id)

        # 2. Deine existierende Methode nutzen (prüft Menge <= 0 und Verfügbarkeit)
        # Wir fangen den ValueError ab und wandeln ihn in ValidationError für Django Forms um
        try:
            stock.ausbuchen(quantity)
        except ValueError as e:
            raise ValidationError(str(e))

        # 3. Bewegung protokollieren
        # ACHTUNG: Dein StockMovement Model hat kein 'user' Feld und kein 'location' Feld.
        # Wir speichern also nur Produkt und Menge.
        StockMovement.objects.create(
            product=stock.product,
            quantity=quantity,
            movement_type='OUT',
            # user=user,  <-- Dein Model hat dieses Feld noch nicht
            # notes=notes <-- Dein Model hat dieses Feld noch nicht
        )

    return stock