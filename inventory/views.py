from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q
from django.db.models import Sum, F
from locationmanager.models import Location
from productmanager.models import Product
from stockmovementmanager.models import  StockMovement
from stockmanager.models import Stock
from ordermanager.models import Order

@login_required
def dashboard(request):
    open_orders_count = Order.objects.filter(status='PENDING').count()
    critical_stock_count = Stock.objects.filter(quantity__lte=F('threshold')).count()

    utilization_rate = 0  # Standardwert

    try:
        # Summe aller Kapazitäten der Lagerplätze
        loc_agg = Location.objects.aggregate(total=Sum('capacity'))
        total_locations = loc_agg['total'] or 0  # 'or 0' fängt None ab, falls DB leer ist

        # Summe aller aktuellen Bestände
        stock_agg = Stock.objects.aggregate(total=Sum('quantity'))
        total_stock = stock_agg['total'] or 0

        # Berechnung: (Aktueller Bestand / Gesamtkapazität) * 100
        if total_locations > 0:
            # Ich habe 'occupied_locations' durch 'total_stock' ersetzt,
            # da du das oben berechnet hast.
            utilization_rate = int((total_stock / total_locations) * 100)
        else:
            utilization_rate = 0

    except Exception as e:
        print(f"Fehler bei der Auslastungsberechnung: {e}")
        utilization_rate = 0

    # D. Letzte Aktivitäten
    try:
        recent_activities = StockMovement.objects.select_related(
            'product',
            'source_location',
            'destination_location'
        ).order_by('-timestamp')[:5]
    except Exception:
        recent_activities = []

    context = {
        "open_orders_count": open_orders_count,
        "critical_stock_count": critical_stock_count,  # <-- Neu im Context
        "utilization_rate": utilization_rate,
        "recent_activities": recent_activities,
    }

    return render(request, 'inventory/index.html', context)