from django.db import transaction
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .models import Stock
from stockmovementmanager.models import StockMovement
from locationmanager.models import Location


# WARENAUSGANG
def process_outgoing_goods(stock_id, quantity, user=None, notes=None):

    if quantity <= 0:
        raise ValidationError("Die Menge muss größer als 0 sein.")

    with transaction.atomic():
        stock = Stock.objects.select_for_update().get(pk=stock_id)

        if stock.quantity < quantity:
            raise ValidationError(f"Nicht genug Bestand! Verfügbar: {stock.quantity}")


        stock.quantity -= quantity
        stock.save()

        StockMovement.objects.create(
            product=stock.product,
            quantity=quantity,
            movement_type='OUT',
            source_location=stock.location,  # Wir wissen, woher es kommt
            destination_location=None  # Ziel ist extern / unbekannt
        )

        return stock


# UMLAGERUNG
def process_stock_transfer(source_stock_id, target_location_id, quantity):

    if quantity <= 0:
        raise ValidationError("Menge muss positiv sein.")

    with transaction.atomic():
        source_stock = Stock.objects.select_for_update().get(pk=source_stock_id)

        if source_stock.quantity < quantity:
            raise ValidationError(f"Zu wenig Bestand. Verfügbar: {source_stock.quantity}")

        source_stock.quantity -= quantity
        source_stock.save()


        target_location = Location.objects.get(pk=target_location_id)


        target_stock, created = Stock.objects.select_for_update().get_or_create(
            product=source_stock.product,
            location=target_location,
            defaults={'quantity': 0, 'threshold': source_stock.threshold}
        )

        target_stock.quantity += quantity
        target_stock.save()


        StockMovement.objects.create(product=source_stock.product,quantity=quantity,movement_type='MOVE',source_location=source_stock.location,destination_location=target_location)
        return source_stock, target_stock