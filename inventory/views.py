from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q
from locationmanager.models import Location
from productmanager.models import Product
from stockmovementmanager.models import  StockMovement
from stockmanager.models import Stock
from ordermanager.models import Order

@login_required
def dashboard(request):
    open_orders_count = Order.objects.filter(status='PENDING').count()
    critical_stock_count = Stock.objects.filter(quantity__lte=F('threshold')).count()

    # C. Lagerauslastung
    try:
        total_locations = Location.objects.count()
        occupied_locations = 0

        if total_locations > 0:
            utilization_rate = int((occupied_locations / total_locations) * 100)
        else:
            utilization_rate = 0
    except Exception:
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