import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db import transaction
from locationmanager.models import Location
from productmanager.models import Product
from .models import Stock, StockMovement



def stock_manager_view(request):

    if request.method == 'POST' and request.POST.get('action') == 'initialize':
        product_id = request.POST.get('product_id')
        location_id = request.POST.get('location_id')
        quantity = request.POST.get('quantity')
        threshold = request.POST.get('threshold')

        if product_id and location_id:
            try:
                prod = Product.objects.get(id=product_id)
                loc = Location.objects.get(id=location_id)

                Stock.objects.update_or_create(
                    product=prod,
                    location=loc,
                    defaults={
                        'quantity': int(quantity),
                        'threshold': int(threshold)
                    }
                )
                messages.success(request, f"Bestand für {prod.name} erfolgreich initialisiert.")
            except Product.DoesNotExist:
                messages.error(request, f"Produkt ID {product_id} nicht gefunden.")
            except Location.DoesNotExist:
                messages.error(request, f"Lagerort ID {location_id} nicht gefunden.")
            except Exception as e:
                messages.error(request, f"Fehler: {str(e)}")

        return redirect('stockmanager/stock_manager')


    stocks = Stock.objects.select_related('product', 'location__warehouse').all()


    all_locations = Location.objects.select_related('warehouse').all()

    context = {
        'stocks': stocks,
        'locations': all_locations
    }
    return render(request, 'stockmanager/stockmanager.html', context)



@require_POST
def book_out_api(request, stock_id):
    try:
        data = json.loads(request.body)
        amount = int(data.get('amount', 0))
        stock = get_object_or_404(Stock, id=stock_id)

        if amount <= 0:
            return JsonResponse({'error': 'Menge muss positiv sein.'}, status=400)
        if stock.quantity < amount:
            return JsonResponse({'error': 'Nicht genügend Bestand verfügbar.'}, status=400)

        with transaction.atomic():
            # Bestand reduzieren
            stock.quantity -= amount
            stock.save()

            StockMovement.objects.create(product=stock.product,source_location=stock.location, destination_location=None,  quantity=amount,movement_type='OUT')

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



@require_POST
def transfer_stock_api(request, stock_id):
    try:
        data = json.loads(request.body)
        amount = int(data.get('amount', 0))
        target_location_id = data.get('target_location_id')

        # Validierung
        if not target_location_id:
            return JsonResponse({'error': 'Kein Ziellagerort gewählt.'}, status=400)

        source_stock = get_object_or_404(Stock, id=stock_id)
        target_location = get_object_or_404(Location, id=target_location_id)

        if amount <= 0 or source_stock.quantity < amount:
            return JsonResponse({'error': 'Ungültige Menge oder zu wenig Bestand.'}, status=400)

        if source_stock.location.id == target_location.id:
            return JsonResponse({'error': 'Start- und Ziellagerort sind identisch.'}, status=400)

        with transaction.atomic():
            # 1. Quelle reduzieren
            source_stock.quantity -= amount
            source_stock.save()

            # 2. Ziel erhöhen oder neu erstellen
            dest_stock, created = Stock.objects.get_or_create(product=source_stock.product,location=target_location,defaults={'quantity': 0, 'threshold': source_stock.threshold})
            dest_stock.quantity += amount
            dest_stock.save()

            # 3. Logging Eintrag (StockMovement)
            StockMovement.objects.create(product=source_stock.product,source_location=source_stock.location,destination_location=target_location,quantity=amount,movement_type='MOVE')

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)